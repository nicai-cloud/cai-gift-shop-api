from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

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

    async def get_all(self):
        inventory_transactions_query = select(
            InventoryTransactionModel.id,
            InventoryTransactionModel.inventory_id,
            InventoryTransactionModel.transaction_type,
            InventoryTransactionModel.quantity
        ).where(InventoryTransactionModel.deleted_at.is_(None))

        result = await self.session.execute(inventory_transactions_query)
        return result.all()

    async def get_by_id(self, inventory_transaction_id: UUID):
        try:
            inventory_transaction_query = select(
                InventoryTransactionModel.id,
                InventoryTransactionModel.inventory_id,
                InventoryTransactionModel.transaction_type,
                InventoryTransactionModel.quantity
            ).where(and_(InventoryTransactionModel.deleted_at.is_(None), InventoryTransactionModel.id == inventory_transaction_id))

            result = await self.session.execute(inventory_transaction_query)
            return result.one()
        except MultipleResultsFound:
            raise InventoryTransactionRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryTransactionRepo.DoesNotExist
    
    async def add(self, inventory_transaction: InventoryTransactionModel):
        self.session.add(inventory_transaction)
        await self.session.flush()


def construct_postgres_inventory_transaction_repo(transactable: PostgresTransactable) -> InventoryTransactionRepo:
    return InventoryTransactionRepo(transactable.session)
