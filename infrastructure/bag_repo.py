from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.bag_model import BagModel


class BagRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self) -> list[BagModel]:
        query = await self.get_filtered_query(BagModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, bag_id: int) -> BagModel:
        try:
            query = await self.get_filtered_query(BagModel)
            query = query.where(BagModel.id == bag_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise BagRepo.MultipleResultsFound
        except NoResultFound:
            raise BagRepo.DoesNotExist


def construct_postgres_bag_repo(transactable: PostgresTransactable) -> BagRepo:
    return BagRepo(transactable.session)
