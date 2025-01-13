import logging

from api.types import ShippingMethod
from infrastructure.shipping_method_repo import ShippingMethodRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class ShippingMethodFeature:
    def __init__(self, work_manager: WorkManager):
        self.shipping_method_repo = work_manager.get(ShippingMethodRepo)
    
    async def get_shipping_methods(self) -> list[ShippingMethod]:
        try:
            shipping_methods = await self.shipping_method_repo.get_all()
            return [ShippingMethod(**shipping_method) for shipping_method in shipping_methods]
        except Exception as e:
            LOG.exception("Unable to get shipping methods due to unexpected error", exc_info=e)

    async def get_shipping_method_by_id(self, shipping_method_id: int) -> ShippingMethod | None:
        try:
            shipping_method = await self.shipping_method_repo.get_by_id(shipping_method_id)
            return ShippingMethod(**shipping_method)
        except ShippingMethodRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get shipping method due to unexpected error", exc_info=e)
