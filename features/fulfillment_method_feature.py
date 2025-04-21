import logging

from api.types import FulfillmentMethod
from infrastructure.fulfillment_method_repo import FulfillmentMethodRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class FulfillmentMethodFeature:
    def __init__(self, work_manager: WorkManager):
        self.fulfillment_method_repo = work_manager.get(FulfillmentMethodRepo)
    
    async def get_fulfillment_methods(self) -> list[FulfillmentMethod]:
        try:
            fulfillment_methods = await self.fulfillment_method_repo.get_all()
            return [FulfillmentMethod(**fulfillment_method) for fulfillment_method in fulfillment_methods]
        except Exception as e:
            LOG.exception("Unable to get fulfillment methods due to unexpected error", exc_info=e)

    async def get_fulfillment_method_by_id(self, fulfillment_method_id: int) -> FulfillmentMethod | None:
        try:
            fulfillment_method = await self.fulfillment_method_repo.get_by_id(fulfillment_method_id)
            return FulfillmentMethod(**fulfillment_method)
        except FulfillmentMethodRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get fulfillment method due to unexpected error", exc_info=e)
