import logging
from uuid import UUID

from api.types import OrderItem
from models.order_item_model import OrderItemModel
from models.custom_bag_items_model import CustomBagItemsModel
from models.custom_bag_order_item_model import CustomBagOrderItemModel
from infrastructure.order_item_repo import OrderItemRepo
from infrastructure.custom_bag_order_item_repo import CustomBagOrderItemRepo
from infrastructure.custom_bag_items_repo import CustomBagItemsRepo
from infrastructure.async_work_management import AsyncWorkManager

LOG = logging.getLogger(__name__)


def construct_order_item(order_item: OrderItemModel) -> OrderItem:
    return OrderItem(
        id=order_item.id,
        quantity=order_item.quantity,
        preselection_id=order_item.preselection_id,
        bag_id=order_item.bag_id,
        item_ids=order_item.item_ids,
        order_id=order_item.order_id
    )


class OrderItemFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.order_item_repo = work_manager.get(OrderItemRepo)
        self.custom_bag_order_item_repo = work_manager.get(CustomBagOrderItemRepo)
        self.custom_bag_items_repo = work_manager.get(CustomBagItemsRepo)

    async def create_preselection_order_item(self, quantity: int, preselection_id: int, order_id: UUID) -> UUID:
        try:
            order_item = OrderItemModel()
            order_item.order_id = order_id
            order_item.quantity = quantity
            order_item.preselection_id = preselection_id
            await self.order_item_repo.add(order_item)
            return order_item.id
        except Exception as e:
            LOG.exception("Unable to create order item due to unexpected error", exc_info=e)
    
    async def create_custom_order_item(self, quantity: int, bag_id: int, item_ids: list[int], order_id: UUID) -> UUID:
        try:
            custom_bag_order_item = CustomBagOrderItemModel()
            await self.custom_bag_order_item_repo.add(custom_bag_order_item)

            for item_id in item_ids:
                custom_bag_items = CustomBagItemsModel()
                custom_bag_items.custom_bag_order_item_id = custom_bag_order_item.id
                custom_bag_items.bag_id = bag_id
                custom_bag_items.item_id = item_id
                await self.custom_bag_items_repo.add(custom_bag_items)

            order_item = OrderItemModel()
            order_item.order_id = order_id
            order_item.quantity = quantity
            order_item.custom_bag_order_item_id = custom_bag_order_item.id
            await self.order_item_repo.add(order_item)
            return order_item.id
        except Exception as e:
            LOG.exception("Unable to create order item due to unexpected error", exc_info=e)

    async def get_order_items(self) -> list[OrderItem]:
        try:
            order_items: list[OrderItemModel] = await self.order_item_repo.get_all()
            return [construct_order_item(order_item) for order_item in order_items]
        except Exception as e:
            LOG.exception("Unable to get order items due to unexpected error", exc_info=e)

    async def get_order_item_by_id(self, order_item_id: UUID) -> OrderItem | None:
        try:
            order_item: OrderItemModel = await self.order_item_repo.get_by_id(order_item_id)
            return construct_order_item(order_item)
        except OrderItemRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get order item due to unexpected error", exc_info=e)
