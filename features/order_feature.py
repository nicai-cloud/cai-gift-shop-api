import logging
from decimal import Decimal
from uuid import UUID

from api.request_types import OrderItemRequest
from api.types import CustomItem, Order, OrderInfo, OrderedItems, PreselectionItem
from features.fulfillment_method_feature import construct_fulfillment_method
from infrastructure.order_repo import OrderRepo
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.preselection_bag_items_repo import PreselectionBagItemsRepo
from infrastructure.bag_repo import BagRepo
from infrastructure.item_repo import ItemRepo
from infrastructure.fulfillment_method_repo import FulfillmentMethodRepo
from infrastructure.coupon_repo import CouponRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.bag_model import BagModel
from models.fulfillment_method_model import FulfillmentMethodModel
from models.item_model import ItemModel
from models.order_model import OrderModel
from models.preselection_model import PreselectionModel
from models.preselection_bag_items_model import PreselectionBagItemsModel
from utils.generate_order_number import generate_order_number
from utils.config import get
from utils.format_number import format_number
from utils.media import get_full_image_url

LOG = logging.getLogger(__name__)


def construct_order(order: OrderModel) -> Order:
    return Order(
        id=order.id,
        customer_id=order.customer_id,
        subtotal=order.subtotal,
        discount=order.discount,
        subtotal_after_discount=order.subtotal_after_discount,
        shipping_cost=order.shipping_cost,
        order_number=order.order_number,
        fulfillment_method=order.fulfillment_method,
        delivery_address=order.delivery_address,
        coupon_id=order.coupon_id
    )


class OrderFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.order_repo = work_manager.get(OrderRepo)
        self.preselection_repo = work_manager.get(PreselectionRepo)
        self.preselection_bag_items_repo = work_manager.get(PreselectionBagItemsRepo)
        self.bag_repo = work_manager.get(BagRepo)
        self.item_repo = work_manager.get(ItemRepo)
        self.fulfillment_method_repo = work_manager.get(FulfillmentMethodRepo)
        self.coupon_repo = work_manager.get(CouponRepo)
    
    async def create_order(self,
        customer_id: UUID,
        subtotal: Decimal,
        discount: Decimal | None,
        subtotal_after_discount: Decimal | None,
        shipping_cost: Decimal,
        fulfillment_method: int,
        delivery_address: str | None,
        coupon_id: str | None
    ) -> tuple[UUID, str]:
        try:
            order_number = generate_order_number()
            order = OrderModel()
            order.customer_id = customer_id
            order.subtotal = subtotal
            order.discount = discount
            order.subtotal_after_discount = subtotal_after_discount
            order.shipping_cost = shipping_cost
            order.order_number = order_number
            order.fulfillment_method = fulfillment_method
            order.delivery_address = delivery_address
            order.coupon_id = coupon_id
            await self.order_repo.add(order)
            return order.id, order_number
        except Exception as e:
            LOG.exception("Unable to create order due to unexpected error", exc_info=e)

    async def calculate_subtotal(self, order_items: list[dict], discount_percentage: int = 0) -> tuple[Decimal, Decimal]:
        subtotal = Decimal(0)
        for order_item in order_items:            
            if order_item.preselection_id:
                preselection: PreselectionModel = await self.preselection_repo.get_by_id(order_item.preselection_id)
                price = preselection.price
            else:
                bag: BagModel = await self.bag_repo.get_by_id(order_item.bag_id)
                price = bag.price
                for item_id in order_item.item_ids:
                    item: ItemModel = await self.item_repo.get_by_id(item_id)
                    price += item.price
            subtotal += price * order_item.quantity
        return (subtotal, subtotal * (Decimal(1) - Decimal(discount_percentage) / Decimal(100)))

    async def calculate_order_quantities(self, order_items: list[OrderItemRequest]) -> tuple[dict[int, int], dict[int, int]]:
        ordered_bag_quantities = {}
        ordered_item_quantities = {}
        for order_item in order_items:
            quantity = order_item.quantity

            if order_item.preselection_id:
                preselection: PreselectionModel = await self.preselection_repo.get_by_id(order_item.preselection_id)
                preselection_bag_items: list[PreselectionBagItemsModel] = await self.preselection_bag_items_repo.get_by_preselection_id(preselection.id)
                ordered_bag_quantities[preselection_bag_items[0].bag_id] = ordered_bag_quantities.get(preselection_bag_items[0].bag_id, 0) + quantity
                for pbi in preselection_bag_items:
                    ordered_item_quantities[pbi.item_id] = ordered_item_quantities.get(pbi.item_id, 0) + quantity
            else:
                ordered_bag_quantities[order_item.bag_id] = ordered_bag_quantities.get(order_item.bag_id, 0) + quantity
                for item_id in order_item.item_ids:
                    ordered_item_quantities[item_id] = ordered_item_quantities.get(item_id, 0) + quantity
        
        return ordered_bag_quantities, ordered_item_quantities

    async def calculate_shipping_cost(self, fulfillment_method_id: int, subtotal: Decimal) -> Decimal:
        free_shipping_threshold = int(get("FREE_SHIPPING_THRESHOLD"))
        fulfillment_method_obj: FulfillmentMethodModel = await self.fulfillment_method_repo.get_by_id(fulfillment_method_id)
        fulfillment_method = construct_fulfillment_method(fulfillment_method_obj)
        return fulfillment_method.discount_fee if subtotal >= free_shipping_threshold else fulfillment_method.fee

    async def get_orders(self) -> list[Order]:
        try:
            orders: list[OrderModel] = await self.order_repo.get_all()
            return [construct_order(order) for order in orders]
        except Exception as e:
            LOG.exception("Unable to get orders due to unexpected error", exc_info=e)

    async def get_order_by_id(self, order_id: UUID) -> Order | None:
        try:
            order: OrderModel = await self.order_repo.get_by_id(order_id)
            return construct_order(order)
        except OrderRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get order due to unexpected error", exc_info=e)

    async def generate_preselection_item(self, index: int, quantity: int, preselection_id: int) -> PreselectionItem:
        try:
            preselection: PreselectionModel = await self.preselection_repo.get_by_id(preselection_id)
            return PreselectionItem(
                index=index,
                image_url=get_full_image_url(preselection.image_url),
                name=preselection.name,
                price=f'${format_number(preselection.price * quantity)}',
                quantity=quantity
            )
        except Exception as e:
            LOG.exception("Unable to get preselection item due to unexpected error", exc_info=e)

    async def generate_custom_item(self, index: int, quantity: int, bag_id: int, item_ids: list[int]) -> CustomItem:
        try:
            bag: BagModel = await self.bag_repo.get_by_id(bag_id)
            items: list[ItemModel] = [await self.item_repo.get_by_id(item_id) for item_id in item_ids]
            unit_price = bag.price + sum(item.price for item in items)
            name = bag.name + ' + ' + ' + '.join([f"{item.name} {item.product}" for item in items])
            return CustomItem(
                index=index,
                name=name,
                price=f"${format_number(unit_price * quantity)}",
                quantity=quantity
            )
        except Exception as e:
            LOG.exception("Unable to get custom item due to unexpected error", exc_info=e)

    async def generate_order_info(self, order_number: str, order_items: dict,  subtotal: Decimal, subtotal_after_discount: Decimal, shipping_cost: Decimal, order_total: Decimal) -> OrderInfo:
        ordered_preselection_items = []
        ordered_custom_items = []
        preselection_index, custom_index = 1, 1
        for order_item in order_items:
            quantity = order_item.quantity

            if order_item.preselection_id:
                preselection_item = await self.generate_preselection_item(preselection_index, quantity, order_item.preselection_id)
                preselection_index += 1
                ordered_preselection_items.append(preselection_item)
            else:
                custom_item = await self.generate_custom_item(custom_index, quantity, order_item.bag_id, order_item.item_ids)
                custom_index += 1
                ordered_custom_items.append(custom_item)

        return OrderInfo(
            order_number=order_number,
            subtotal=subtotal,
            subtotal_after_discount=subtotal_after_discount,
            shipping_cost=shipping_cost,
            order_total=order_total,
            ordered_items=OrderedItems(
                preselection_items=ordered_preselection_items,
                custom_items=ordered_custom_items
            )
        )
