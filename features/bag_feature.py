import logging

from api.types import BagWithInventory
from infrastructure.bag_repo import BagRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class BagFeature:
    def __init__(self, work_manager: WorkManager):
        self.bag_repo = work_manager.get(BagRepo)
    
    async def get_bags(self) -> list[BagWithInventory]:
        try:
            bags = await self.bag_repo.get_all()
            return [BagWithInventory(**bag) for bag in bags]
        except Exception as e:
            LOG.exception("Unable to get bags due to unexpected error", exc_info=e)

    async def get_bag_by_id(self, bag_id: int) -> BagWithInventory:
        try:
            bag = await self.bag_repo.get_by_id(bag_id)
            return BagWithInventory(**bag)
        except Exception as e:
            LOG.exception("Unable to get bag due to unexpected error", exc_info=e)

    async def get_out_of_stock_bags(self) -> list[int]:
        try:
            out_of_stock_bags = await self.bag_repo.get_out_of_stock_bags()
            return out_of_stock_bags
        except Exception as e:
            LOG.exception("Unable to get out of stock bags due to unexpected error", exc_info=e)
