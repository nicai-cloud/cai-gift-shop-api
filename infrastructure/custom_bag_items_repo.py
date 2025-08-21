from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.custom_bag_items_model import CustomBagItemsModel


class CustomBagItemsRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def add(self, custom_bag_items: CustomBagItemsModel):
        self.session.add(custom_bag_items)
        await self.session.flush()


def construct_postgres_custom_bag_items_repo(transactable: PostgresTransactable) -> CustomBagItemsRepo:
    return CustomBagItemsRepo(transactable.session)
