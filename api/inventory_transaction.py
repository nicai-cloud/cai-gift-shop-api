from uuid import UUID
from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetInventoryTransactionsResponse, GetInventoryTransactionResponse
from features.inventory_transaction_feature import InventoryTransactionFeature
from infrastructure.async_work_management import AsyncWorkManager


class InventoryTransactionRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.inventory_transaction_feature = InventoryTransactionFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_inventory_transactions(self, req, resp):
        inventory_transactions = await self.inventory_transaction_feature.get_inventory_transactions()
        resp.media = GetInventoryTransactionsResponse(inventory_transactions=inventory_transactions)
        resp.status = HTTP_OK

    @route.get("/{inventory_transaction_id}", auth_exempt=True)
    async def get_inventory_transaction_by_id(self, req, resp, inventory_transaction_id):
        try:
            inventory_transaction_id = UUID(inventory_transaction_id)
        except ValueError:
            raise HTTPBadRequest(
                title="Invalid parameter",
                description="The 'inventory_transaction_id' must be a valid UUID."
            )

        inventory_transaction = await self.inventory_transaction_feature.get_inventory_transaction_by_id(inventory_transaction_id)
        
        if inventory_transaction is None:
            raise NotFound(detail=f"Inventory Transaction with inventory_transaction_id {inventory_transaction_id} not found.")
    
        resp.media = GetInventoryTransactionResponse(inventory_transaction=inventory_transaction)
        resp.status = HTTP_OK
