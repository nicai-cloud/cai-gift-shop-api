from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import update

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

    async def get_all(self) -> list[InventoryModel]:
        query = await self.get_filtered_query(InventoryModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, inventory_id: int) -> InventoryModel:
        try:
            query = await self.get_filtered_query(InventoryModel)
            query = query.where(InventoryModel.id == inventory_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise InventoryRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryRepo.DoesNotExist
    
    async def get_by_bag_id(self, bag_id: int) -> InventoryModel:
        try:
            query = await self.get_filtered_query(InventoryModel)
            query = query.where(InventoryModel.entity_type == "bag", InventoryModel.entity_id == bag_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise InventoryRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryRepo.DoesNotExist

    async def get_by_item_id(self, item_id: int) -> InventoryModel:
        try:
            query = await self.get_filtered_query(InventoryModel)
            query = query.where(InventoryModel.entity_type == "item", InventoryModel.entity_id == item_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise InventoryRepo.MultipleResultsFound
        except NoResultFound:
            raise InventoryRepo.DoesNotExist
    
    async def update(self, inventory_id: int, new_inventory: dict):
        update_query = update(InventoryModel).where(InventoryModel.id == inventory_id).values(**new_inventory)
        await self.session.execute(update_query)


def construct_postgres_inventory_repo(transactable: PostgresTransactable) -> InventoryRepo:
    return InventoryRepo(transactable.session)
