from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.preselection_model import PreselectionModel
from models.types import Preselection
from utils.object_mapping import map_to_dataclass, map_to_dataclasses


class PreselectionRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    @map_to_dataclasses(Preselection)
    async def get_all(self) -> list[Preselection]:
        preselections_query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(preselections_query)
        
        preselections = result.scalars().all()
        return preselections
    
    @map_to_dataclass(Preselection)
    async def get(self, preselection_id: int) -> Preselection:
        preselection_query = await self.get_filtered_query(PreselectionModel)
        result = await self.session.execute(preselection_query.where(PreselectionModel.id == preselection_id))
            
        preselection = result.scalars().first()
        return preselection


def construct_postgres_preselection_repo(transactable: PostgresTransactable) -> PreselectionRepo:
    return PreselectionRepo(transactable.session)
