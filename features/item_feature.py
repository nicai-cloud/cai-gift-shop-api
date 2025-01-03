from collections import defaultdict
import logging

from api.types import ItemWithInventory
from infrastructure.item_repo import ItemRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class ItemFeature:
    def __init__(self, work_manager: WorkManager):
        self.item_repo = work_manager.get(ItemRepo)
    
    async def get_items(self) -> list[ItemWithInventory]:
        try:
            items = await self.item_repo.get_all()
            return [ItemWithInventory(**item) for item in items]
        except Exception as e:
            LOG.exception("Unable to get items due to unexpected error", exc_info=e)
    
    async def get_items_with_category(self) -> dict[str, list[ItemWithInventory]]:
        try:
            items = await self.item_repo.get_all_with_sorting()
            items_dict = defaultdict(list)
            for item in items:
                items_dict[item["category"]].append(ItemWithInventory(**item))
            return dict(items_dict)
        except Exception as e:
            LOG.exception("Unable to get items due to unexpected error", exc_info=e)

    async def get_item(self, item_id: int) -> ItemWithInventory:
        try:
            item = await self.item_repo.get_by_id(item_id)
            return ItemWithInventory(**item)
        except Exception as e:
            LOG.exception("Unable to get item due to unexpected error", exc_info=e)

    async def get_out_of_stock_items(self) -> list[int]:
        try:
            out_of_stock_items = await self.item_repo.get_out_of_stock_items()
            return out_of_stock_items
        except Exception as e:
            LOG.exception("Unable to get out of stock items due to unexpected error", exc_info=e)
