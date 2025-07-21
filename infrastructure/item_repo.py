from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.item_model import ItemModel


class ItemRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self) -> list[ItemModel]:
        query = await self.get_filtered_query(ItemModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_all_with_sorting(self) -> list[ItemModel]:
        query = await self.get_filtered_query(ItemModel)
        query = query.order_by(ItemModel.product, ItemModel.name)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, item_id: int) -> ItemModel:
        try:
            query = await self.get_filtered_query(ItemModel)
            query = query.where(ItemModel.id == item_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise ItemRepo.MultipleResultsFound
        except NoResultFound:
            raise ItemRepo.DoesNotExist


def construct_postgres_item_repo(transactable: PostgresTransactable) -> ItemRepo:
    return ItemRepo(transactable.session)
