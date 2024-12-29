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
    async def get_inventory_by_id(self, req, resp, inventory_id):
        resp.media = await self.inventory_feature.get_inventory_by_id(int(inventory_id))
        resp.status = falcon.HTTP_OK

    @route.get("/", auth_exempt=True)
    async def get_inventory_by_bag_or_item_id(self, req, resp):
        bag_id = req.params.get('bagId')
        item_id = req.params.get('itemId')
        if bag_id:
            resp.media = await self.inventory_feature.get_inventory_by_bag_id(int(bag_id))
        elif item_id:
            resp.media = await self.inventory_feature.get_inventory_by_item_id(int(item_id))
        resp.status = falcon.HTTP_OK

    @route.post("/refill-bags", auth_exempt=True)
    async def refill_bags(self, req, resp):
        request_body = await req.get_media()
        bag_id = request_body["bag_id"]
        quantity = request_body["quantity"]
        await self.inventory_feature.refill_bags(bag_id, quantity)
        resp.status = falcon.HTTP_OK

    @route.post("/refill-items", auth_exempt=True)
    async def refill_items(self, req, resp):
        request_body = await req.get_media()
        item_id = request_body["item_id"]
        quantity = request_body["quantity"]
        await self.inventory_feature.refill_items(item_id, quantity)
        resp.status = falcon.HTTP_OK
