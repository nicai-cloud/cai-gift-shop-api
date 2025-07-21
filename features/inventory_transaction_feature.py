import logging
from uuid import UUID

from api.types import InventoryTransaction
from infrastructure.inventory_transaction_repo import InventoryTransactionRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.inventory_transaction_model import InventoryTransactionModel

LOG = logging.getLogger(__name__)


def construct_inventory_transaction(inventory_transaction: InventoryTransactionModel) -> InventoryTransaction:
    return InventoryTransaction(
        id=inventory_transaction.id,
        inventory_id=inventory_transaction.inventory_id,
        transaction_type=inventory_transaction.transaction_type,
        quantity=inventory_transaction.quantity
    )


class InventoryTransactionFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.inventory_transaction_repo = work_manager.get(InventoryTransactionRepo)
    
    async def get_inventory_transactions(self) -> list[InventoryTransaction]:
        try:
            inventory_transactions: list[InventoryTransactionModel] = await self.inventory_transaction_repo.get_all()
            return [construct_inventory_transaction(inventory_transaction) for inventory_transaction in inventory_transactions]
        except Exception as e:
            LOG.exception("Unable to get inventory transactions due to unexpected error", exc_info=e)

    async def get_inventory_transaction_by_id(self, inventory_transaction_id: UUID) -> InventoryTransaction | None:
        try:
            inventory_transaction: InventoryTransactionModel = await self.inventory_transaction_repo.get_by_id(inventory_transaction_id)
            return construct_inventory_transaction(inventory_transaction)
        except InventoryTransactionRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory transaction due to unexpected error", exc_info=e)
