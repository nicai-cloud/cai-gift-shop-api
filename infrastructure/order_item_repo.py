from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.order_item_model import OrderItemModel


class OrderItemRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def add(self, order: OrderItemModel):
        self.session.add(order)
        await self.session.flush()

    async def get_all(self) -> list[OrderItemModel]:
        query = await self.get_filtered_query(OrderItemModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, order_item_id: UUID) -> OrderItemModel:
        try:
            query = await self.get_filtered_query(OrderItemModel)
            query = query.where(OrderItemModel.id == order_item_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise OrderItemRepo.MultipleResultsFound
        except NoResultFound:
            raise OrderItemRepo.DoesNotExist


def construct_postgres_order_item_repo(transactable: PostgresTransactable) -> OrderItemRepo:
    return OrderItemRepo(transactable.session)
