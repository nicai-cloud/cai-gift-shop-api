from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.request_types import OrderItemsRequest, RefillItemRequest
from features.inventory_feature import InventoryFeature
from infrastructure.work_management import WorkManager
import marshmallow


class InventoryRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.inventory_feature = InventoryFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_inventories(self, req, resp):
        resp.media = await self.inventory_feature.get_inventories()
        resp.status = HTTP_OK

    @route.get("/search", auth_exempt=True)
    async def get_inventory_by_id_or_bag_id_or_item_id(self, req, resp):
        id = req.params.get('id')
        bag_id = req.params.get('bagId')
        item_id = req.params.get('itemId')
        if id:
            inventory = await self.inventory_feature.get_inventory_by_id(int(id))
        elif bag_id:
            inventory = await self.inventory_feature.get_inventory_by_bag_id(int(bag_id))
        elif item_id:
            inventory = await self.inventory_feature.get_inventory_by_item_id(int(item_id))

        if inventory is None:
            raise NotFound(detail=f"Inventory of id ({id}) or bag_id ({bag_id}) or item_id ({item_id}) not found.")
    
        resp.media = inventory
        resp.status = HTTP_OK

    @route.post("/refill-bags", auth_exempt=True)
    async def refill_bags(self, req, resp):
        raw_request_body = await req.get_media()

        try:
            request_body = OrderItemsRequest.Schema().load(raw_request_body)
        except marshmallow.exceptions.ValidationError as e:
            raise HTTPBadRequest(title="Invalid request payload", description=str(e))

        bag_id = request_body.bag_id
        quantity = request_body.quantity
        await self.inventory_feature.refill_bags(bag_id, quantity)
        resp.status = HTTP_OK

    @route.post("/refill-items", auth_exempt=True)
    async def refill_items(self, req, resp):
        raw_request_body = await req.get_media()

        try:
            request_body = RefillItemRequest.Schema().load(raw_request_body)
        except marshmallow.exceptions.ValidationError as e:
            raise HTTPBadRequest(title="Invalid request payload", description=str(e))

        item_id = request_body.item_id
        quantity = request_body.quantity
        await self.inventory_feature.refill_items(item_id, quantity)
        resp.status = HTTP_OK
