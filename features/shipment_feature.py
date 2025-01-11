import logging
from uuid import UUID
from datetime import date

from api.types import Shipment
from infrastructure.shipment_repo import ShipmentRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class ShipmentFeature:
    def __init__(self, work_manager: WorkManager):
        self.shipment_repo = work_manager.get(ShipmentRepo)
    
    async def get_shipments(self) -> list[Shipment]:
        try:
            shipments = await self.shipment_repo.get_all()
            return [Shipment(**shipment) for shipment in shipments]
        except Exception as e:
            LOG.exception("Unable to get shipments due to unexpected error", exc_info=e)

    async def get_shipment_by_order_id(self, order_id: UUID) -> Shipment:
        try:
            shipment = await self.shipment_repo.get_by_order_id(order_id)
            return Shipment(**shipment)
        except Exception as e:
            LOG.exception("Unable to get shipment due to unexpected error", exc_info=e)

    async def create_shipment(self, volume: float | None, weight: float, delivery_fee: float, tracking_number: str, order_id: UUID) -> UUID:
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
        except Exception as e:
            LOG.exception("Unable to get shipment due to unexpected error", exc_info=e)
