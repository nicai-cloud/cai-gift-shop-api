import falcon

from api.base import RequestHandler, route
from features.order_item_feature import OrderItemFeature
from infrastructure.work_management import WorkManager


class OrderItemRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.order_item_feature = OrderItemFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_order_items(self, req, resp):
        resp.media = await self.order_item_feature.get_order_items()
        resp.status = falcon.HTTP_OK

    @route.get("/{order_item_id}", auth_exempt=True)
    async def get_order_item(self, req, resp, order_item_id):
        resp.media = await self.order_item_feature.get_order_item_by_id(order_item_id)
        resp.status = falcon.HTTP_OK
