from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

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
    
    async def get_all(self):
        shipments_query = select(
            ShipmentModel.id,
            ShipmentModel.volume,
            ShipmentModel.weight,
            ShipmentModel.delivery_fee,
            ShipmentModel.send_date,
            ShipmentModel.receive_date,
            ShipmentModel.tracking_number,
            ShipmentModel.order_id
        ).where(ShipmentModel.deleted_at.is_(None))

        result = await self.session.execute(shipments_query)
        return result.all()
    
    async def get_by_order_id(self, order_id: UUID):
        try:
            shipment_query = select(
                ShipmentModel.id,
                ShipmentModel.volume,
                ShipmentModel.weight,
                ShipmentModel.delivery_fee,
                ShipmentModel.send_date,
                ShipmentModel.receive_date,
                ShipmentModel.tracking_number,
                ShipmentModel.order_id
            ).where(and_(ShipmentModel.deleted_at.is_(None), ShipmentModel.order_id == order_id))

            result = await self.session.execute(shipment_query)
            return result.one()
        except MultipleResultsFound:
            raise ShipmentRepo.MultipleResultsFound
        except NoResultFound:
            raise ShipmentRepo.DoesNotExist
    
    async def create(self, shipment: dict) -> UUID:
        create_shipment_stmt = insert(ShipmentModel).values(shipment)
        shipment_entry = await self.session.execute(create_shipment_stmt)
        return shipment_entry.inserted_primary_key[0]


def construct_postgres_shipment_repo(transactable: PostgresTransactable) -> ShipmentRepo:
    return ShipmentRepo(transactable.session)
