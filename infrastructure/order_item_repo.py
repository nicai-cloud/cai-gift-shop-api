from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.order_item_model import OrderItemModel


class OrderItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, order: dict) -> UUID:
        create_order_item_stmt = insert(OrderItemModel).values(order)
        order_item_entry = await self.session.execute(create_order_item_stmt)
        return order_item_entry.inserted_primary_key[0]

    async def get_all(self):
        order_items_query = await self.get_filtered_query(OrderItemModel)
        result = await self.session.execute(order_items_query)
        
        return result.scalars().all()
    
    async def get_by_id(self, order_item_id: str):
        order_item_query = await self.get_filtered_query(OrderItemModel)
        result = await self.session.execute(order_item_query.where(OrderItemModel.id == order_item_id))
            
        order_item = result.scalars().first()
        return order_item


def construct_postgres_order_item_repo(transactable: PostgresTransactable) -> OrderItemRepo:
    return OrderItemRepo(transactable.session)
