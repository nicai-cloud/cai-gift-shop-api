import logging

from api.types import InventoryTransaction
from infrastructure.inventory_transaction_repo import InventoryTransactionRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class InventoryTransactionFeature:
    def __init__(self, work_manager: WorkManager):
        self.inventory_transaction_repo = work_manager.get(InventoryTransactionRepo)
    
    async def get_inventory_transactions(self) -> list[InventoryTransaction]:
        try:
            inventory_transactions = await self.inventory_transaction_repo.get_all()
            return [InventoryTransaction(**inventory_transaction.to_dict()) for inventory_transaction in inventory_transactions]
        except Exception as e:
            LOG.exception("Unable to get inventory transactions due to unexpected error", exc_info=e)

    async def get_inventory_transaction(self, inventory_transaction_id: int) -> InventoryTransaction:
        try:
            inventory_transaction = await self.inventory_transaction_repo.get_by_id(inventory_transaction_id)
            return InventoryTransaction(**inventory_transaction.to_dict())
        except Exception as e:
            LOG.exception("Unable to get inventory transaction due to unexpected error", exc_info=e)
