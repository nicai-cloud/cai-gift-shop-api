from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

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

    async def add(self, order: OrderModel):
        self.session.add(order)
        await self.session.flush()

    async def get_all(self) -> list[OrderModel]:
        query = await self.get_filtered_query(OrderModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, order_id: UUID) -> OrderModel:
        try:
            query = await self.get_filtered_query(OrderModel)
            query = query.where(OrderModel.id == order_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise OrderRepo.MultipleResultsFound
        except NoResultFound:
            raise OrderRepo.DoesNotExist


def construct_postgres_order_repo(transactable: PostgresTransactable) -> OrderRepo:
    return OrderRepo(transactable.session)
