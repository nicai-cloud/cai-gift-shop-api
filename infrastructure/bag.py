from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.bag_model import BagModel


class BagRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, bag: dict) -> int:
        create_bag_stmt = insert(BagModel).values(bag)
        bag_entry = await self.session.execute(create_bag_stmt)
        return bag_entry.inserted_primary_key[0]


def construct_postgres_bag_repo(transactable: PostgresTransactable) -> BagRepo:
    return BagRepo(transactable.session)
