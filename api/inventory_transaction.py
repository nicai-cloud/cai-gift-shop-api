from uuid import UUID
from falcon import HTTP_OK, HTTPNotFound

from api.base import RequestHandler, route
from features.inventory_transaction_feature import InventoryTransactionFeature
from infrastructure.work_management import WorkManager


class InventoryTransactionRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.inventory_transaction_feature = InventoryTransactionFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_inventory_transactions(self, req, resp):
        resp.media = await self.inventory_transaction_feature.get_inventory_transactions()
        resp.status = HTTP_OK

    @route.get("/{inventory_transaction_id}", auth_exempt=True)
    async def get_inventory_transaction_by_id(self, req, resp, inventory_transaction_id):
        inventory_transaction = await self.inventory_transaction_feature.get_inventory_transaction(UUID(inventory_transaction_id))
        
        if inventory_transaction is None:
            raise HTTPNotFound(description="Inventory Transaction not found")
    
        resp.media = inventory_transaction
        resp.status = HTTP_OK
