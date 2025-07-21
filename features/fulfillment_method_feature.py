import logging

from api.types import FulfillmentMethod
from infrastructure.fulfillment_method_repo import FulfillmentMethodRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.fulfillment_method_model import FulfillmentMethodModel

LOG = logging.getLogger(__name__)


def construct_fulfillment_method(fulfillment_method: FulfillmentMethodModel) -> FulfillmentMethod:
    return FulfillmentMethod(
        id=fulfillment_method.id,
        name=fulfillment_method.name,
        fee=fulfillment_method.fee,
        discount_fee=fulfillment_method.discount_fee
    )


class FulfillmentMethodFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.fulfillment_method_repo = work_manager.get(FulfillmentMethodRepo)
    
    async def get_fulfillment_methods(self) -> list[FulfillmentMethod]:
        try:
            fulfillment_methods: list[FulfillmentMethodModel] = await self.fulfillment_method_repo.get_all()
            return [construct_fulfillment_method(fulfillment_method) for fulfillment_method in fulfillment_methods]
        except Exception as e:
            LOG.exception("Unable to get fulfillment methods due to unexpected error", exc_info=e)

    async def get_fulfillment_method_by_id(self, fulfillment_method_id: int) -> FulfillmentMethod | None:
        try:
            fulfillment_method: FulfillmentMethodModel = await self.fulfillment_method_repo.get_by_id(fulfillment_method_id)
            return construct_fulfillment_method(fulfillment_method)
        except FulfillmentMethodRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get fulfillment method due to unexpected error", exc_info=e)
