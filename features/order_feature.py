import logging
from uuid import UUID
from infrastructure.order import OrderRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class OrderFeature:
    def __init__(self, work_manager: WorkManager):
        self.order_repo = work_manager.get(OrderRepo)
    
    async def create_order(self, customer_id, order_item_ids) -> UUID:
        try:
            order = {
                "customer_id": customer_id,
                "order_item_ids": order_item_ids
            }
            return await self.order_repo.create(order)
        except Exception as e:
            LOG.exception("Unable to create order due to unexpected error", exc_info=e)
