from uuid import UUID
from falcon import HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from features.order_feature import OrderFeature
from infrastructure.work_management import WorkManager


class OrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.order_feature = OrderFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_orders(self, req, resp):
        resp.media = await self.order_feature.get_orders()
        resp.status = HTTP_OK

    @route.get("/{order_id}", auth_exempt=True)
    async def get_order(self, req, resp, order_id):
        order = await self.order_feature.get_order_by_id(UUID(order_id))
        if order is None:
            raise NotFound(detail=f"Order with order_id {order_id} not found.")
    
        resp.media = order
        resp.status = HTTP_OK
