import logging

from api.types import Inventory
from infrastructure.inventory_repo import InventoryRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class InventoryFeature:
    def __init__(self, work_manager: WorkManager):
        self.inventory_repo = work_manager.get(InventoryRepo)
    
    async def get_inventories(self) -> list[Inventory]:
        try:
            inventories = await self.inventory_repo.get_all()
            return [Inventory(**inventory.to_dict()) for inventory in inventories]
        except Exception as e:
            LOG.exception("Unable to get inventories due to unexpected error", exc_info=e)

    async def get_inventory(self, inventory_id: int) -> Inventory:
        try:
            inventory = await self.inventory_repo.get_by_id(inventory_id)
            return Inventory(**inventory.to_dict())
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)
