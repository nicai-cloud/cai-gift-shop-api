from uuid import UUID
from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetOrderResponse, GetOrdersResponse
from features.order_feature import OrderFeature
from infrastructure.work_management import WorkManager


class OrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.order_feature = OrderFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_orders(self, req, resp):
        orders = await self.order_feature.get_orders()
        resp.media = GetOrdersResponse(orders=orders)
        resp.status = HTTP_OK

    @route.get("/{order_id}", auth_exempt=True)
    async def get_order(self, req, resp, order_id):
        try:
            order_id = UUID(order_id)
        except ValueError:
            raise HTTPBadRequest(
                title="Invalid parameter",
                description="The 'order_id' must be a valid UUID."
            )

        order = await self.order_feature.get_order_by_id(order_id)
        if order is None:
            raise NotFound(detail=f"Order with order_id {order_id} not found.")
    
        resp.media = GetOrderResponse(order=order)
        resp.status = HTTP_OK
