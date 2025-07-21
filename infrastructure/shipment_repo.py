from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.shipment_model import ShipmentModel


class ShipmentRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self) -> list[ShipmentModel]:
        query = await self.get_filtered_query(ShipmentModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    
    async def get_by_order_id(self, order_id: UUID) -> ShipmentModel:
        try:
            query = await self.get_filtered_query(ShipmentModel)
            query = query.where(ShipmentModel.order_id == order_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise ShipmentRepo.MultipleResultsFound
        except NoResultFound:
            raise ShipmentRepo.DoesNotExist
    
    async def add(self, shipment: ShipmentModel):
        self.session.add(shipment)
        await self.session.flush()


def construct_postgres_shipment_repo(transactable: PostgresTransactable) -> ShipmentRepo:
    return ShipmentRepo(transactable.session)
