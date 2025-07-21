from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetInventoriesResponse, GetInventoryResponse
from api.request_types import RefillBagRequest, RefillItemRequest
from features.inventory_feature import InventoryFeature
from infrastructure.async_work_management import AsyncWorkManager
import marshmallow


class InventoryRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.inventory_feature = InventoryFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_inventories(self, req, resp):
        inventories = await self.inventory_feature.get_inventories()
        resp.media = GetInventoriesResponse(inventories=inventories)
        resp.status = HTTP_OK

    @route.get("/search", auth_exempt=True)
    async def get_inventory_by_id_or_bag_id_or_item_id(self, req, resp):
        id = req.params.get('id')
        bag_id = req.params.get('bag-id')
        item_id = req.params.get('item-id')
        inventory = None
        if id:
            try:
                id = int(id)
            except ValueError:
                raise HTTPBadRequest(
                    title="Invalid parameter",
                    description="The 'id' must be a valid integer."
                )
            inventory = await self.inventory_feature.get_inventory_by_id(id)
        elif bag_id:
            try:
                bag_id = int(bag_id)
            except ValueError:
                raise HTTPBadRequest(
                    title="Invalid parameter",
                    description="The 'bag_id' must be a valid integer."
                )
            inventory = await self.inventory_feature.get_inventory_by_bag_id(bag_id)
        elif item_id:
            try:
                item_id = int(item_id)
            except ValueError:
                raise HTTPBadRequest(
                    title="Invalid parameter",
                    description="The 'item_id' must be a valid integer."
                )
            inventory = await self.inventory_feature.get_inventory_by_item_id(item_id)

        if inventory is None:
            raise NotFound(detail=f"Inventory of id ({id}) or bag-id ({bag_id}) or item-id ({item_id}) not found.")
    
        resp.media = GetInventoryResponse(inventory=inventory)
        resp.status = HTTP_OK

    @route.post("/refill-bags", auth_exempt=True)
    async def refill_bags(self, req, resp):
        raw_request_body = await req.get_media()

        try:
            request_body = RefillBagRequest.Schema().load(raw_request_body)
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
