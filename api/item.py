from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetItemsResponse, GetItemResponse, GetItemsWithProductResponse
from features.item_feature import ItemFeature
from infrastructure.work_management import WorkManager


class ItemRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.item_feature = ItemFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_items(self, req, resp):
        items = await self.item_feature.get_items()
        resp.media = GetItemsResponse(items=items)
        resp.status = HTTP_OK
    
    @route.get("/with-product", auth_exempt=True)
    async def get_items_with_product(self, req, resp):
        items_with_product = await self.item_feature.get_items_with_product()
        resp.media = GetItemsWithProductResponse(items_with_product=items_with_product)
        resp.status = HTTP_OK

    @route.get("/{item_id}", auth_exempt=True)
    async def get_item(self, req, resp, item_id):
        try:
            item_id = int(item_id)
        except ValueError:
            raise HTTPBadRequest(
                title="Invalid parameter",
                description="The 'item_id' must be a valid integer."
            )

        item = await self.item_feature.get_item(item_id)
        if item is None:
            raise NotFound(detail=f"Item with item_id {item_id} not found.")

        resp.media = GetItemResponse(item=item)
        resp.status = HTTP_OK
