import logging
from uuid import UUID
from infrastructure.order_item import OrderItemRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class OrderItemFeature:
    def __init__(self, work_manager: WorkManager):
        self.order_item_repo = work_manager.get(OrderItemRepo)
    
    async def create_order_item(self, customer_id, order_item_id) -> UUID:
        try:
            order_item = {
                "customer_id": customer_id,
                "order_item_id": order_item_id
            }
            return await self.order_item_repo.create(order_item)
        except Exception as e:
            LOG.exception("Unable to create order due to unexpected error", exc_info=e)
