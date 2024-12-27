from collections import defaultdict
import logging

from api.types import Item
from infrastructure.item_repo import ItemRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class ItemFeature:
    def __init__(self, work_manager: WorkManager):
        self.item_repo = work_manager.get(ItemRepo)
    
    async def get_items(self) -> list[Item]:
        try:
            items = await self.item_repo.get_all()
            return [Item(**item.to_dict()) for item in items]
        except Exception as e:
            LOG.exception("Unable to get items due to unexpected error", exc_info=e)
    
    async def get_items_with_category(self) -> dict[str, list[Item]]:
        try:
            items = await self.item_repo.get_all()
            items_dict = defaultdict(list)
            for item in items:
                item_dict = item.to_dict()
                items_dict[item_dict["category"]].append(Item(**item_dict))
            return dict(items_dict)
        except Exception as e:
            LOG.exception("Unable to get items due to unexpected error", exc_info=e)

    async def get_item(self, item_id: int) -> Item:
        try:
            item = await self.item_repo.get_by_id(item_id)
            return Item(**item.to_dict())
        except Exception as e:
            LOG.exception("Unable to get item due to unexpected error", exc_info=e)
