from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.order_model import OrderModel


class OrderRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, order: dict) -> UUID:
        create_order_stmt = insert(OrderModel).values(order)
        order_entry = await self.session.execute(create_order_stmt)
        return order_entry.inserted_primary_key[0]


def construct_postgres_order_repo(transactable: PostgresTransactable) -> OrderRepo:
    return OrderRepo(transactable.session)
