from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.order_model import OrderModel


class OrderRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, order: dict) -> UUID:
        create_order_stmt = insert(OrderModel).values(order)
        order_entry = await self.session.execute(create_order_stmt)
        return order_entry.inserted_primary_key[0]

    async def get_all(self):
        orders_query = await self.get_filtered_query(OrderModel)
        result = await self.session.execute(orders_query)
        
        return result.scalars().all()
    
    async def get_by_id(self, order_id: UUID):
        try:
            order_query = await self.get_filtered_query(OrderModel)
            result = await self.session.execute(order_query.where(OrderModel.id == order_id))
            
            order = result.scalar_one()
            return order
        except MultipleResultsFound:
            raise OrderRepo.MultipleResultsFound
        except NoResultFound:
            raise OrderRepo.DoesNotExist


def construct_postgres_order_repo(transactable: PostgresTransactable) -> OrderRepo:
    return OrderRepo(transactable.session)
