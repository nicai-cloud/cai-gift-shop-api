import logging
from uuid import UUID
from datetime import date

from api.types import Customer, Order, Shipment
from infrastructure.shipment_repo import ShipmentRepo
from infrastructure.order_repo import OrderRepo
from infrastructure.customer_repo import CustomerRepo
from infrastructure.work_management import WorkManager
from sqlalchemy.exc import IntegrityError

LOG = logging.getLogger(__name__)


class ShipmentAlreadyExistsException(Exception):
    def __init__(self, order_id):
        super().__init__(f"Shipment already exists for order_id: {order_id}")


class ShipmentFeature:
    def __init__(self, work_manager: WorkManager):
        self.shipment_repo = work_manager.get(ShipmentRepo)
        self.order_repo = work_manager.get(OrderRepo)
        self.customer_repo = work_manager.get(CustomerRepo)
    
    async def get_shipments(self) -> list[Shipment]:
        try:
            shipments = await self.shipment_repo.get_all()
            return [Shipment(**shipment) for shipment in shipments]
        except Exception as e:
            LOG.exception("Unable to get shipments due to unexpected error", exc_info=e)

    async def get_shipment_by_order_id(self, order_id: UUID) -> Shipment | None:
        try:
            shipment = await self.shipment_repo.get_by_order_id(order_id)
            return Shipment(**shipment)
        except ShipmentRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get shipment due to unexpected error", exc_info=e)
    
    async def get_customer(self, order_id: UUID) -> Customer | None:
        try:
            order_obj = await self.order_repo.get_by_id(order_id)
            order = Order(**order_obj)
            customer_obj = await self.customer_repo.get_by_id(order.customer_id)
            return Customer(**customer_obj)
        except OrderRepo.DoesNotExist:
            return None
        except CustomerRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get customer due to unexpected error", exc_info=e)

    async def create_shipment(self, volume: float | None, weight: float, delivery_fee: float, tracking_number: str, order_id: UUID) -> UUID | None:
        # Ensure a shipment for the same order_id hasn't been created yet
        shipment = await self.shipment_repo.get_by_order_id(order_id)
        if shipment is not None:
            raise ShipmentAlreadyExistsException(order_id)
        
        try:
            shipment_dict = {
                "volume": volume,
                "weight": weight,
                "delivery_fee": delivery_fee,
                "send_date": date.today(),
                "tracking_number": tracking_number,
                "order_id": order_id
            }
            return await self.shipment_repo.create(shipment_dict)
        except IntegrityError as e:
            return None
        except Exception as e:
            LOG.exception("Unable to create shipment due to unexpected error", exc_info=e)
