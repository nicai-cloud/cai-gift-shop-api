from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.inventory_transaction_model import InventoryTransactionModel


class InventoryTransactionRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self) -> list[InventoryTransactionModel]:
        query = await self.get_filtered_query(InventoryTransactionModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, inventory_transaction_id: UUID) -> InventoryTransactionModel:
        try:
            query = await self.get_filtered_query(InventoryTransactionModel)
            query = query.where(InventoryTransactionModel.id == inventory_transaction_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise InventoryTransactionRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryTransactionRepo.DoesNotExist
    
    async def add(self, inventory_transaction: InventoryTransactionModel):
        self.session.add(inventory_transaction)
        await self.session.flush()


def construct_postgres_inventory_transaction_repo(transactable: PostgresTransactable) -> InventoryTransactionRepo:
    return InventoryTransactionRepo(transactable.session)
