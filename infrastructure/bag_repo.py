from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.bag_model import BagModel


class BagRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self):
        bags_query = await self.get_filtered_query(BagModel)
        result = await self.session.execute(bags_query)
        
        return result.scalars().all()
    
    async def get_by_id(self, bag_id: int):
        bag_query = await self.get_filtered_query(BagModel)
        result = await self.session.execute(bag_query.where(BagModel.id == bag_id))
            
        bag = result.scalars().first()
        return bag


def construct_postgres_bag_repo(transactable: PostgresTransactable) -> BagRepo:
    return BagRepo(transactable.session)
