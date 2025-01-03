from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.bag_model import BagModel
from models.inventory_model import InventoryModel


class BagRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self):
        bags_with_inventory_query = (
            select(
                BagModel.id,
                BagModel.image_url,
                BagModel.name,
                BagModel.description,
                BagModel.price,
                InventoryModel.current_stock
            )
            .join(InventoryModel, BagModel.id == InventoryModel.entity_id)
            .where(and_(BagModel.deleted_at.is_(None), InventoryModel.entity_type == "bag"))
        )
        result = await self.session.execute(bags_with_inventory_query)
        
        return result.all()
    
    async def get_by_id(self, bag_id: int):
        bag_with_inventory_query = (
            select(
                BagModel.id,
                BagModel.image_url,
                BagModel.name,
                BagModel.description,
                BagModel.price,
                InventoryModel.current_stock
            )
            .join(InventoryModel, BagModel.id == InventoryModel.entity_id)
            .where(and_(BagModel.deleted_at.is_(None), InventoryModel.entity_type == "bag", BagModel.id == bag_id))
        )
        result = await self.session.execute(bag_with_inventory_query)
        return result.first()


def construct_postgres_bag_repo(transactable: PostgresTransactable) -> BagRepo:
    return BagRepo(transactable.session)
