import logging
from infrastructure.item_repo import ItemRepo
from infrastructure.work_management import WorkManager
from models.types import Item

LOG = logging.getLogger(__name__)


class ItemFeature:
    def __init__(self, work_manager: WorkManager):
        self.item_repo = work_manager.get(ItemRepo)
    
    async def get_items(self) -> list[Item]:
        try:
            return await self.item_repo.get_all()
        except Exception as e:
            LOG.exception("Unable to get items due to unexpected error", exc_info=e)

    async def get_item(self, item_id: int) -> Item:
        try:
            return await self.item_repo.get(item_id)
        except Exception as e:
            LOG.exception("Unable to get item due to unexpected error", exc_info=e)
