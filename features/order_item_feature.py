import logging
from uuid import UUID

from api.types import OrderItem
from infrastructure.order_item_repo import OrderItemRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class OrderItemFeature:
    def __init__(self, work_manager: WorkManager):
        self.order_item_repo = work_manager.get(OrderItemRepo)
    
    async def create_order_item(self, quantity: int, preselection_id: int, bag_id: int, item_ids: list[int], order_id: UUID) -> UUID:
        try:
            order_item = {
                "order_id": order_id,
                "quantity": quantity
            }

            if preselection_id:
                order_item.update({
                    "preselection_id": preselection_id
                })
            elif bag_id and item_ids:
                order_item.update({
                    "bag_id": bag_id,
                    "item_ids": item_ids
                })
            return await self.order_item_repo.create(order_item)
        except Exception as e:
            LOG.exception("Unable to create order item due to unexpected error", exc_info=e)

    async def get_order_items(self) -> list[OrderItem]:
        try:
            order_items = await self.order_item_repo.get_all()
            return [OrderItem(**order_item) for order_item in order_items]
        except Exception as e:
            LOG.exception("Unable to get order items due to unexpected error", exc_info=e)

    async def get_order_item_by_id(self, order_item_id: UUID) -> OrderItem:
        try:
            order_item = await self.order_item_repo.get_by_id(order_item_id)
            return OrderItem(**order_item)
        except OrderItemRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get order item due to unexpected error", exc_info=e)
