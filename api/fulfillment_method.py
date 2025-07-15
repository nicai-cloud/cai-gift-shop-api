from falcon import HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetFulfillmentMethodResponse, GetFulfillmentMethodsResponse
from features.fulfillment_method_feature import FulfillmentMethodFeature
from infrastructure.async_work_management import AsyncWorkManager
from utils.config import get


class FulfillmentMethodRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.fulfillment_method_feature = FulfillmentMethodFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_fulfillment_methods(self, req, resp):
        fulfillment_methods = await self.fulfillment_method_feature.get_fulfillment_methods()
        resp.media = GetFulfillmentMethodsResponse(fulfillment_methods=fulfillment_methods, free_shipping_threshold=f'{get("FREE_SHIPPING_THRESHOLD")}')
        resp.status = HTTP_OK

    @route.get("/{id:int}", auth_exempt=True)
    async def get_fulfillment_method_by_id(self, req, resp, id):
        fulfillment_method = await self.fulfillment_method_feature.get_fulfillment_method_by_id(id)
        if fulfillment_method is None:
            raise NotFound(detail=f"Fulfillment method id {id} not found.")
        
        resp.media = GetFulfillmentMethodResponse(fulfillment_method=fulfillment_method)
        resp.status = HTTP_OK
