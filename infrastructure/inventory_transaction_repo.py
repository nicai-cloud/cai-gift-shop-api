from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.inventory_transaction_model import InventoryTransactionModel


class InventoryTransactionRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        inventory_transactions_query = await self.get_filtered_query(InventoryTransactionModel)
        result = await self.session.execute(inventory_transactions_query)
        
        return result.scalars().all()

    async def get_by_id(self, inventory_transaction_id: str):
        inventory_transaction_query = await self.get_filtered_query(InventoryTransactionModel)
        result = await self.session.execute(inventory_transaction_query.where(InventoryTransactionRepo.id == inventory_transaction_id))
            
        return result.scalars().first()
    
    async def create(self, inventory_transaction: dict):
        create_inventory_transaction_stmt = insert(InventoryTransactionModel).values(inventory_transaction)
        inventory_transaction_entry = await self.session.execute(create_inventory_transaction_stmt)
        return inventory_transaction_entry.inserted_primary_key[0]


def construct_postgres_inventory_transaction_repo(transactable: PostgresTransactable) -> InventoryTransactionRepo:
    return InventoryTransactionRepo(transactable.session)
