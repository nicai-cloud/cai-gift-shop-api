from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.inventory_model import InventoryModel


class InventoryRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        inventories_query = await self.get_filtered_query(InventoryModel)
        result = await self.session.execute(inventories_query)
        
        return result.scalars().all()

    async def get_by_id(self, inventory_id: int):
        inventory_query = await self.get_filtered_query(InventoryModel)
        result = await self.session.execute(inventory_query.where(InventoryModel.id == inventory_id))
            
        return result.scalars().first()


def construct_postgres_inventory_repo(transactable: PostgresTransactable) -> InventoryRepo:
    return InventoryRepo(transactable.session)
