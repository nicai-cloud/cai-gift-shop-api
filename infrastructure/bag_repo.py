from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

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
    
    async def get_all(self):
        bags_query = select(
            BagModel.id,
            BagModel.image_url,
            BagModel.video_url,
            BagModel.name,
            BagModel.description,
            BagModel.price
        ).where(BagModel.deleted_at.is_(None))

        result = await self.session.execute(bags_query)
        return result.all()
    
    async def get_by_id(self, bag_id: int):
        try:
            bag_query = select(
                BagModel.id,
                BagModel.image_url,
                BagModel.video_url,
                BagModel.name,
                BagModel.description,
                BagModel.price
            ).where(and_(BagModel.deleted_at.is_(None), BagModel.id == bag_id))

            result = await self.session.execute(bag_query)
            return result.one()
        except MultipleResultsFound:
            raise BagRepo.MultipleResultsFound
        except NoResultFound:
            raise BagRepo.DoesNotExist


def construct_postgres_bag_repo(transactable: PostgresTransactable) -> BagRepo:
    return BagRepo(transactable.session)
