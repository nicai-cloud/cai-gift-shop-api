from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import update, and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.inventory_model import InventoryModel


class InventoryRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        inventories_query = select(
            InventoryModel.id,
            InventoryModel.entity_type,
            InventoryModel.entity_id,
            InventoryModel.current_stock,
            InventoryModel.low_stock_threshold
        ).where(InventoryModel.deleted_at.is_(None))
        result = await self.session.execute(inventories_query)
        
        return result.all()

    async def get_by_id(self, inventory_id: int):
        try:
            inventory_query = select(
                InventoryModel.id,
                InventoryModel.entity_type,
                InventoryModel.entity_id,
                InventoryModel.current_stock,
                InventoryModel.low_stock_threshold
            ).where(and_(InventoryModel.deleted_at.is_(None)), InventoryModel.id == inventory_id)
            
            result = await self.session.execute(inventory_query)
            return result.one()
        except MultipleResultsFound:
            raise InventoryRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryRepo.DoesNotExist
    
    async def get_by_bag_id(self, bag_id: int):
        try:
            inventory_query = select(
                InventoryModel.id,
                InventoryModel.entity_type,
                InventoryModel.entity_id,
                InventoryModel.current_stock,
                InventoryModel.low_stock_threshold
            ).where(and_(InventoryModel.deleted_at.is_(None)), InventoryModel.entity_type == "bag", InventoryModel.entity_id == bag_id)
            
            result = await self.session.execute(inventory_query)
            return result.one()
        except MultipleResultsFound:
            raise InventoryRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryRepo.DoesNotExist

    async def get_by_item_id(self, item_id: int):
        try:
            inventory_query = select(
                InventoryModel.id,
                InventoryModel.entity_type,
                InventoryModel.entity_id,
                InventoryModel.current_stock,
                InventoryModel.low_stock_threshold
            ).where(and_(InventoryModel.deleted_at.is_(None)), InventoryModel.entity_type == "item", InventoryModel.entity_id == item_id)
            
            result = await self.session.execute(inventory_query)
            return result.one()
        except MultipleResultsFound:
            raise InventoryRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryRepo.DoesNotExist
    
    async def update(self, inventory_id: int, new_inventory: dict):
        update_query = update(InventoryModel).where(InventoryModel.id == inventory_id).values(**new_inventory)
        await self.session.execute(update_query)


def construct_postgres_inventory_repo(transactable: PostgresTransactable) -> InventoryRepo:
    return InventoryRepo(transactable.session)
