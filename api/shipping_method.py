from falcon import HTTP_OK, HTTPNotFound

from api.base import RequestHandler, route
from features.shipping_method_feature import ShippingMethodFeature
from infrastructure.work_management import WorkManager


class ShippingMethodRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.shipping_method_feature = ShippingMethodFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_shipping_methods(self, req, resp):
        resp.media = await self.shipping_method_feature.get_shipping_methods()
        resp.status = HTTP_OK

    @route.get("/", auth_exempt=True)
    async def get_shipping_method_by_id(self, req, resp):
        shipping_method_id = req.params.get('shippingMethodId')
        shipping_method = await self.shipping_method_feature.get_shipping_method_by_id(int(shipping_method_id))
        if shipping_method is None:
            raise HTTPNotFound(description="Shipping method not found")
        
        resp.media = shipping_method
        resp.status = HTTP_OK
