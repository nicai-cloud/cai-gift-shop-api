from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.item_model import ItemModel


class ItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        items_query = await self.get_filtered_query(ItemModel)
        result = await self.session.execute(items_query)
        
        return result.scalars().all()

    async def get_by_id(self, item_id: int):
        item_query = await self.get_filtered_query(ItemModel)
        result = await self.session.execute(item_query.where(ItemModel.id == item_id))
            
        return result.scalars().first()


def construct_postgres_item_repo(transactable: PostgresTransactable) -> ItemRepo:
    return ItemRepo(transactable.session)
