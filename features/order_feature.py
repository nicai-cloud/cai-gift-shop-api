import logging
from uuid import UUID
from infrastructure.order_repo import OrderRepo
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.bag_repo import BagRepo
from infrastructure.item_repo import ItemRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class OrderFeature:
    def __init__(self, work_manager: WorkManager):
        self.order_repo = work_manager.get(OrderRepo)
        self.preselection_repo = work_manager.get(PreselectionRepo)
        self.bag_repo = work_manager.get(BagRepo)
        self.item_repo = work_manager.get(ItemRepo)
    
    async def create_order(self, customer_id: UUID, order_item_ids: list[UUID], amount: float) -> UUID:
        try:
            order = {
                "customer_id": customer_id,
                "order_item_ids": order_item_ids,
                "amount": amount
            }
            return await self.order_repo.create(order)
        except Exception as e:
            LOG.exception("Unable to create order due to unexpected error", exc_info=e)

    async def calculate_total_cost(self, order_items: list[dict]) -> float:
        total_cost = 0
        for order_item in order_items:
            quantity = order_item["quantity"]
            price = 0
            if "preselection_id" in order_item:
                preselection_id = order_item["preselection_id"]
                preselection = await self.preselection_repo.get(preselection_id)
                price = preselection.price
            elif "bag_id" in order_item and "item_ids" in order_item:
                bag_id = order_item["bag_id"]
                bag = await self.bag_repo.get(bag_id)
                price = bag.price

                item_ids = order_item["item_ids"]
                for item_id in item_ids:
                    item = await self.item_repo.get(item_id)
                    price += item.price
            total_cost += price * quantity
        return total_cost
