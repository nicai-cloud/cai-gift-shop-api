from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.item_model import ItemModel
from models.inventory_model import InventoryModel


class ItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        items_with_inventory_query = (
            select(
                ItemModel.id,
                ItemModel.image_url,
                ItemModel.name,
                ItemModel.description,
                ItemModel.price,
                ItemModel.category,
                InventoryModel.current_stock
            )
            .join(InventoryModel, ItemModel.id == InventoryModel.entity_id)
            .where(and_(ItemModel.deleted_at.is_(None), InventoryModel.entity_type == "item"))
        )
        result = await self.session.execute(items_with_inventory_query)
        
        return result.all()
    
    async def get_all_with_sorting(self):
        items_with_inventory_query_and_sorting = (
            select(
                ItemModel.id,
                ItemModel.image_url,
                ItemModel.name,
                ItemModel.description,
                ItemModel.price,
                ItemModel.category,
                InventoryModel.current_stock
            )
            .join(InventoryModel, ItemModel.id == InventoryModel.entity_id)
            .where(and_(ItemModel.deleted_at.is_(None), InventoryModel.entity_type == "item"))
            .order_by(ItemModel.category, ItemModel.name)
        )
        result = await self.session.execute(items_with_inventory_query_and_sorting)
        
        return result.all()

    async def get_by_id(self, item_id: int):
        item_with_inventory_query = (
            select(
                ItemModel.id,
                ItemModel.image_url,
                ItemModel.name,
                ItemModel.description,
                ItemModel.price,
                ItemModel.category,
                InventoryModel.current_stock
            )
            .join(InventoryModel, ItemModel.id == InventoryModel.entity_id)
            .where(and_(ItemModel.deleted_at.is_(None), InventoryModel.entity_type == "item", ItemModel.id == item_id))
        )
        result = await self.session.execute(item_with_inventory_query)
            
        return result.first()


    async def get_out_of_stock_items(self):
        out_of_stock_items_query = (
            select(ItemModel.id)
            .join(InventoryModel, ItemModel.id == InventoryModel.entity_id)
            .where(and_(ItemModel.deleted_at.is_(None), InventoryModel.entity_type == "item", InventoryModel.current_stock == 0))
        )
        result = await self.session.execute(out_of_stock_items_query)
        return result.scalars().all()

def construct_postgres_item_repo(transactable: PostgresTransactable) -> ItemRepo:
    return ItemRepo(transactable.session)
