from falcon import HTTP_OK, HTTPNotFound

from api.base import RequestHandler, route
from features.item_feature import ItemFeature
from infrastructure.work_management import WorkManager


class ItemRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.item_feature = ItemFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_items(self, req, resp):
        resp.media = await self.item_feature.get_items()
        resp.status = HTTP_OK
    
    @route.get("/all-with-product", auth_exempt=True)
    async def get_items_with_product(self, req, resp):
        resp.media = await self.item_feature.get_items_with_product()
        resp.status = HTTP_OK

    @route.get("/{item_id}", auth_exempt=True)
    async def get_item(self, req, resp, item_id):
        item = await self.item_feature.get_item(int(item_id))
        if item is None:
            raise HTTPNotFound(description="Item not found")

        resp.media = item
        resp.status = HTTP_OK
