from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

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

    async def get_all(self):
        preselections_query = select(
            PreselectionModel.id,
            PreselectionModel.image_url,
            PreselectionModel.video_url,
            PreselectionModel.name,
            PreselectionModel.gender,
            PreselectionModel.description,
            PreselectionModel.price,
            PreselectionModel.bag_id,
            PreselectionModel.item_ids
        ).where(PreselectionModel.deleted_at.is_(None))

        result = await self.session.execute(preselections_query)
        return result.all()

    async def get_by_name(self, preselection_name: str):
        try:
            preselection_query = select(
                PreselectionModel.id,
                PreselectionModel.image_url,
                PreselectionModel.video_url,
                PreselectionModel.name,
                PreselectionModel.gender,
                PreselectionModel.description,
                PreselectionModel.price,
                PreselectionModel.bag_id,
                PreselectionModel.item_ids
            ).where(and_(PreselectionModel.deleted_at.is_(None), PreselectionModel.name == preselection_name))

            result = await self.session.execute(preselection_query)
            print('!!', result)
            return result.one()
        except MultipleResultsFound:
            raise PreselectionRepo.MultipleResultsFound
        except NoResultFound:
            raise PreselectionRepo.DoesNotExist


def construct_postgres_preselection_repo(transactable: PostgresTransactable) -> PreselectionRepo:
    return PreselectionRepo(transactable.session)
