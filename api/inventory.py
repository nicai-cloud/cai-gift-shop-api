import falcon

from api.base import RequestHandler, route
from features.inventory_feature import InventoryFeature
from infrastructure.work_management import WorkManager


class InventoryRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.inventory_feature = InventoryFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_inventories(self, req, resp):
        resp.media = await self.inventory_feature.get_inventories()
        resp.status = falcon.HTTP_OK

    @route.get("/{inventory_id}", auth_exempt=True)
    async def get_inventory(self, req, resp, inventory_id):
        resp.media = await self.inventory_feature.get_inventory(int(inventory_id))
        resp.status = falcon.HTTP_OK
