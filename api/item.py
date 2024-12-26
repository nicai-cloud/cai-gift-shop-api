import falcon

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
        resp.status = falcon.HTTP_OK
    
    @route.get("/all-by-sub-category", auth_exempt=True)
    async def get_items_by_sub_category(self, req, resp):
        resp.media = await self.item_feature.get_items_by_sub_category()
        resp.status = falcon.HTTP_OK

    @route.get("/{item_id}", auth_exempt=True)
    async def get_item(self, req, resp, item_id):
        resp.media = await self.item_feature.get_item(int(item_id))
        resp.status = falcon.HTTP_OK
