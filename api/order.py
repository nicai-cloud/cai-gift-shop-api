import falcon

from api.base import RequestHandler, route
from features.order_feature import OrderFeature
from infrastructure.work_management import WorkManager


class OrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.order_feature = OrderFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_orders(self, req, resp):
        resp.media = await self.order_feature.get_orders()
        resp.status = falcon.HTTP_OK

    @route.get("/{order_id}", auth_exempt=True)
    async def get_order(self, req, resp, order_id):
        resp.media = await self.order_feature.get_order_by_id(order_id)
        resp.status = falcon.HTTP_OK
