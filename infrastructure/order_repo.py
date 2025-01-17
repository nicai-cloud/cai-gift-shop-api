from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

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

    async def get_all(self):
        orders_query = select(
            OrderModel.id,
            OrderModel.customer_id,
            OrderModel.subtotal,
            OrderModel.discount,
            OrderModel.subtotal_after_discount,
            OrderModel.shipping_cost,
            OrderModel.order_number,
            OrderModel.shipping_method,
            OrderModel.coupon_id
        ).where(OrderModel.deleted_at.is_(None))
        result = await self.session.execute(orders_query)
        
        return result.all()
    
    async def get_by_id(self, order_id: UUID):
        try:
            order_query = select(
                OrderModel.id,
                OrderModel.customer_id,
                OrderModel.subtotal,
                OrderModel.discount,
                OrderModel.subtotal_after_discount,
                OrderModel.shipping_cost,
                OrderModel.order_number,
                OrderModel.shipping_method,
                OrderModel.coupon_id
            ).where(and_(OrderModel.deleted_at.is_(None), OrderModel.id == order_id))
            
            result = await self.session.execute(order_query)
            return result.one()
        except MultipleResultsFound:
            raise OrderRepo.MultipleResultsFound
        except NoResultFound:
            raise OrderRepo.DoesNotExist


def construct_postgres_order_repo(transactable: PostgresTransactable) -> OrderRepo:
    return OrderRepo(transactable.session)
