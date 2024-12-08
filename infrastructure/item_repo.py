from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.item_model import ItemModel
from models.types import Item
from utils.object_mapping import map_to_dataclass, map_to_dataclasses


class ItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    @map_to_dataclasses(Item)
    async def get_all(self) -> list[Item]:
        items_query = await self.get_filtered_query(ItemModel)
        result = await self.session.execute(items_query)
        
        items = result.scalars().all()
        return items

    @map_to_dataclass(Item)
    async def get(self, item_id: int) -> Item:
        item_query = await self.get_filtered_query(ItemModel)
        result = await self.session.execute(item_query.where(ItemModel.id == item_id))
            
        item = result.scalars().first()
        return item


def construct_postgres_item_repo(transactable: PostgresTransactable) -> ItemRepo:
    return ItemRepo(transactable.session)
