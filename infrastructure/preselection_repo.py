from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.preselection_model import PreselectionModel


class PreselectionRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        preselections_query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(preselections_query)
        
        return result.scalars().all()
    
    async def get_by_id(self, preselection_id: int):
        preselection_query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(preselection_query.where(PreselectionModel.id == preselection_id))
            
        return result.scalars().first()

    async def get_by_name(self, preselection_name: str):
        preselection_query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(preselection_query.where(PreselectionModel.name == preselection_name))
            
        return result.scalars().first()


def construct_postgres_preselection_repo(transactable: PostgresTransactable) -> PreselectionRepo:
    return PreselectionRepo(transactable.session)
