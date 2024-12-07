from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.item_model import ItemModel


class ItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, item: dict) -> int:
        create_item_stmt = insert(ItemModel).values(item)
        item_entry = await self.session.execute(create_item_stmt)
        return item_entry.inserted_primary_key[0]


def construct_postgres_item_repo(transactable: PostgresTransactable) -> ItemRepo:
    return ItemRepo(transactable.session)
