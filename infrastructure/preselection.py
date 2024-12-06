from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.preselection_model import PreselectionModel


class PreSelectItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        preselection_query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(preselection_query)
            
        preselections = result.scalars().all()
        return preselections


def construct_postgres_preselection_repo(transactable: PostgresTransactable) -> PreSelectItemRepo:
    return PreSelectItemRepo(transactable.session)
