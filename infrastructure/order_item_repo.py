from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

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

    async def get_all(self):
        order_items_query = select(
            OrderItemModel.id,
            OrderItemModel.quantity,
            OrderItemModel.preselection_id,
            OrderItemModel.bag_id,
            OrderItemModel.item_ids,
            OrderItemModel.order_id
        ).where(OrderItemModel.deleted_at.is_(None))

        result = await self.session.execute(order_items_query)
        return result.all()
    
    async def get_by_id(self, order_item_id: UUID):
        try:
            order_item_query = select(
                OrderItemModel.id,
                OrderItemModel.quantity,
                OrderItemModel.preselection_id,
                OrderItemModel.bag_id,
                OrderItemModel.item_ids,
                OrderItemModel.order_id
            ).where(and_(OrderItemModel.deleted_at.is_(None), OrderItemModel.id == order_item_id))

            result = await self.session.execute(order_item_query)
            return result.one()
        except MultipleResultsFound:
            raise OrderItemRepo.MultipleResultsFound
        except NoResultFound:
            raise OrderItemRepo.DoesNotExist


def construct_postgres_order_item_repo(transactable: PostgresTransactable) -> OrderItemRepo:
    return OrderItemRepo(transactable.session)
