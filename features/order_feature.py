import logging
from uuid import UUID

from api.types import Bag, Item, Order, ShippingMethod
from infrastructure.order_repo import OrderRepo
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.bag_repo import BagRepo
from infrastructure.item_repo import ItemRepo
from infrastructure.shipping_method_repo import ShippingMethodRepo
from infrastructure.work_management import WorkManager
from utils.generate_order_number import generate_order_number
from utils.config import get

LOG = logging.getLogger(__name__)


class OrderFeature:
    def __init__(self, work_manager: WorkManager):
        self.order_repo = work_manager.get(OrderRepo)
        self.preselection_repo = work_manager.get(PreselectionRepo)
        self.bag_repo = work_manager.get(BagRepo)
        self.item_repo = work_manager.get(ItemRepo)
        self.shipping_method_repo = work_manager.get(ShippingMethodRepo)
    
    async def create_order(self, customer_id: UUID, shipping_method: int, subtotal: float, shipping_cost: float) -> tuple[UUID, str]:
        try:
            order_number = generate_order_number()
            order = {
                "customer_id": customer_id,
                "subtotal": subtotal,
                "shipping_cost": shipping_cost,
                "order_number": order_number,
                "shipping_method": shipping_method
            }
            return await self.order_repo.create(order), order_number
        except Exception as e:
            LOG.exception("Unable to create order due to unexpected error", exc_info=e)

    async def calculate_subtotal(self, order_items: list[dict]) -> float:
        subtotal = 0
        for order_item in order_items:
            quantity = order_item["quantity"]
            price = 0
            if "preselection_id" in order_item:
                preselection_id = order_item["preselection_id"]
                preselection = await self.preselection_repo.get_by_id(preselection_id)
                price = preselection.price
            elif "bag_id" in order_item and "item_ids" in order_item:
                bag_id = order_item["bag_id"]
                bag = await self.bag_repo.get_by_id(bag_id)
                price = bag.price

                item_ids = order_item["item_ids"]
                for item_id in item_ids:
                    item = await self.item_repo.get_by_id(item_id)
                    price += item.price
            subtotal += price * quantity
        return subtotal

    async def calculate_order_quantities(self, order_items: list[dict]) -> tuple[dict, dict]:
        bag_quantities = {}
        item_quantities = {}
        for order_item in order_items:
            quantity = order_item["quantity"]

            bag_id = order_item.get("bag_id", None)
            item_ids = order_item.get("item_ids", None)
            if bag_id and item_ids:
                bag_quantities[bag_id] = bag_quantities.get(bag_id, 0) + quantity
                for item_id in item_ids:
                    item_quantities[item_id] = item_quantities.get(item_id, 0) + quantity

            preselection_id = order_item.get("preselection_id", None)
            if preselection_id:
                preselection = await self.preselection_repo.get_by_id(preselection_id)
                bag_quantities[preselection.bag_id] = bag_quantities.get(preselection.bag_id, 0) + quantity
                for preselection_item_id in preselection.item_ids:
                    item_quantities[preselection_item_id] = item_quantities.get(preselection_item_id, 0) + quantity
        
        return bag_quantities, item_quantities

    async def calculate_shipping_cost(self, shipping_method_id: int, subtotal: float) -> float:
        discount_threshold = int(get("DISCOUNT_THRESHOLD"))
        shipping_method_obj = await self.shipping_method_repo.get_by_id(shipping_method_id)
        shipping_method = ShippingMethod(**shipping_method_obj)
        return shipping_method.discount_fee if subtotal >= discount_threshold else shipping_method.fee

    async def get_orders(self) -> list[Order]:
        try:
            orders = await self.order_repo.get_all()
            return [Order(**order) for order in orders]
        except Exception as e:
            LOG.exception("Unable to get orders due to unexpected error", exc_info=e)

    async def get_order_by_id(self, order_id: UUID) -> Order | None:
        try:
            order = await self.order_repo.get_by_id(order_id)
            return Order(**order)
        except OrderRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get order due to unexpected error", exc_info=e)

    async def generate_preselection_item_payload(self, index: int, quantity: int, preselection_id: int):
        try:
            preselection = await self.preselection_repo.get_by_id(preselection_id)
            return {
                "index": index,
                "image_url": preselection["image_url"],
                "name": preselection["name"],
                "price": preselection["price"] * quantity,
                "quantity": quantity
            }
        except Exception as e:
            LOG.exception("Unable to get preselection item due to unexpected error", exc_info=e)

    async def _calculate_customer_gift_unit_price(self, bag: Bag, items: list[Item]):
        return bag.price + sum(item.price for item in items)
    
    async def _generate_custom_gift_name(self, bag: Bag, items: list[Item]):
        return bag.name + ' + ' + ' + '.join([f"{item.name} {item.product}" for item in items])

    async def generate_custom_item_payload(self, index: int, quantity: int, bag_id: int, item_ids: list[int]):
        try:
            bag = Bag(**(await self.bag_repo.get_by_id(bag_id)))
            items = [Item(**(await self.item_repo.get_by_id(item_id))) for item_id in item_ids]
            return {
                "index": index,
                "name": await self._generate_custom_gift_name(bag, items),
                "quantity": quantity,
                "price": (await self._calculate_customer_gift_unit_price(bag, items)) * quantity
            }
        except Exception as e:
            LOG.exception("Unable to get custom item due to unexpected error", exc_info=e)

    async def generate_order_info(self, order_number: str, order_items: dict,  subtotal: float, shipping_cost: float, order_total: float) -> dict:
        ordered_preselection_items = []
        ordered_custom_items = []
        preselection_index, custom_index = 1, 1
        for order_item in order_items:
            quantity = order_item["quantity"]
            preselection_id = order_item.get("preselection_id", None)
            bag_id = order_item.get("bag_id", None)
            item_ids = order_item.get("item_ids", None)

            if preselection_id:
                preselection_item = await self.generate_preselection_item_payload(preselection_index, quantity, preselection_id)
                preselection_index += 1
                ordered_preselection_items.append(preselection_item)
            if bag_id and item_ids:
                custom_item = await self.generate_custom_item_payload(custom_index, quantity, bag_id, item_ids)
                custom_index += 1
                ordered_custom_items.append(custom_item)

        order_info = {
            "order_number": order_number,
            "subtotal": subtotal,
            "shipping_cost": shipping_cost,
            "order_total": order_total,
            "ordered_items": {
                "preselection_items": ordered_preselection_items,
                "custom_items": ordered_custom_items
            }
        }
        return order_info
