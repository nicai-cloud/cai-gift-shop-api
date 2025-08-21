from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.custom_bag_order_item_model import CustomBagOrderItemModel


class CustomBagOrderItemRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def add(self, custom_bag_order_item: CustomBagOrderItemModel):
        self.session.add(custom_bag_order_item)
        await self.session.flush()


def construct_postgres_custom_bag_order_item_repo(transactable: PostgresTransactable) -> CustomBagOrderItemRepo:
    return CustomBagOrderItemRepo(transactable.session)
