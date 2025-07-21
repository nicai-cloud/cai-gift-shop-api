from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.preselection_model import PreselectionModel


class PreselectionRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self) -> list[PreselectionModel]:
        query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, preselection_id: int) -> PreselectionModel:
        try:
            query = await self.get_filtered_query(PreselectionModel)
            query = query.where(PreselectionModel.id == preselection_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise PreselectionRepo.MultipleResultsFound
        except NoResultFound:
            raise PreselectionRepo.DoesNotExist

    async def get_by_name(self, preselection_name: str) -> PreselectionModel:
        try:
            query = await self.get_filtered_query(PreselectionModel)
            query = query.where(PreselectionModel.name == preselection_name)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise PreselectionRepo.MultipleResultsFound
        except NoResultFound:
            raise PreselectionRepo.DoesNotExist


def construct_postgres_preselection_repo(transactable: PostgresTransactable) -> PreselectionRepo:
    return PreselectionRepo(transactable.session)
