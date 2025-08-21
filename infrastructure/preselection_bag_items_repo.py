from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.preselection_bag_items_model import PreselectionBagItemsModel


class PreselectionBagItemsRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_by_preselection_id(self, preselection_id: int) -> list[PreselectionBagItemsModel]:
        try:
            query = await self.get_filtered_query(PreselectionBagItemsModel)
            query = query.where(PreselectionBagItemsModel.preselection_id == preselection_id)
            result = await self.session.execute(query)
            return result.scalars().all()
        except NoResultFound:
            raise PreselectionBagItemsRepo.DoesNotExist


def construct_postgres_preselection_bag_items_repo(transactable: PostgresTransactable) -> PreselectionBagItemsRepo:
    return PreselectionBagItemsRepo(transactable.session)
