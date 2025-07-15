from uuid import UUID
from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetOrderItemResponse, GetOrderItemsResponse
from features.order_item_feature import OrderItemFeature
from infrastructure.async_work_management import AsyncWorkManager


class OrderItemRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.order_item_feature = OrderItemFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_order_items(self, req, resp):
        order_items = await self.order_item_feature.get_order_items()
        resp.media = GetOrderItemsResponse(order_items=order_items)
        resp.status = HTTP_OK

    @route.get("/{order_item_id}", auth_exempt=True)
    async def get_order_item(self, req, resp, order_item_id):
        try:
            order_item_id = UUID(order_item_id)
        except ValueError:
            raise HTTPBadRequest(
                title="Invalid parameter",
                description="The 'order_item_id' must be a valid UUID."
            )

        order_item = await self.order_item_feature.get_order_item_by_id(order_item_id)
        if order_item is None:
            raise NotFound(detail=f"Order item with order_item_id {order_item_id} not found.")

        resp.media = GetOrderItemResponse(order_item=order_item)
        resp.status = HTTP_OK
