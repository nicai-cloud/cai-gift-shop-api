from collections import defaultdict
import logging

from api.types import Inventory
from infrastructure.inventory_repo import InventoryRepo
from infrastructure.inventory_transaction_repo import InventoryTransactionRepo
from infrastructure.work_management import WorkManager
from dataclasses import asdict

LOG = logging.getLogger(__name__)


class InventoryFeature:
    def __init__(self, work_manager: WorkManager):
        self.inventory_repo = work_manager.get(InventoryRepo)
        self.inventory_transactoin_repo = work_manager.get(InventoryTransactionRepo)
    
    async def get_inventories(self):
        try:
            inventories = await self.inventory_repo.get_all()
            inventories_dict = defaultdict(dict[str, int])
            for inventory in inventories:
                inventories_dict[inventory["entity_type"]].update({inventory["entity_id"]: inventory["current_stock"]})
            return dict(inventories_dict)
        except Exception as e:
            LOG.exception("Unable to get inventories due to unexpected error", exc_info=e)

    async def get_inventory_by_id(self, inventory_id: int) -> Inventory | None:
        try:
            inventory = await self.inventory_repo.get_by_id(inventory_id)
            return Inventory(**inventory)
        except InventoryRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)

    async def get_inventory_by_bag_id(self, bag_id: int) -> Inventory | None:
        try:
            inventory = await self.inventory_repo.get_by_bag_id(bag_id)
            return Inventory(**inventory)
        except InventoryRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)

    async def get_inventory_by_item_id(self, item_id: int) -> Inventory | None:
        try:
            inventory = await self.inventory_repo.get_by_item_id(item_id)
            return Inventory(**inventory)
        except InventoryRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)
    
    async def refill_bags(self, bag_id: int, quantity: int):
        try:
            bag_inventory = await self.inventory_repo.get_by_bag_id(bag_id)
            bag_inventory_dict = asdict(Inventory(**bag_inventory))
            bag_inventory_dict["current_stock"] += quantity
            await self.inventory_repo.update(bag_inventory.id, bag_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = {
                "inventory_id": bag_inventory.id,
                "transaction_type": "refill",
                "quantity": quantity
            }
            await self.inventory_transactoin_repo.create(inventory_transaction)
        except Exception as e:
            LOG.exception("Unable to refill bags due to unexpected error", exc_info=e)
    
    async def refill_items(self, item_id: int, quantity: int):
        try:
            item_inventory = await self.inventory_repo.get_by_item_id(item_id)
            item_inventory_dict = asdict(Inventory(**item_inventory))
            item_inventory_dict["current_stock"] += quantity
            await self.inventory_repo.update(item_inventory.id, item_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = {
                "inventory_id": item_inventory.id,
                "transaction_type": "refill",
                "quantity": quantity
            }
            await self.inventory_transactoin_repo.create(inventory_transaction)
        except Exception as e:
            LOG.exception("Unable to refill items due to unexpected error", exc_info=e)
    
    async def update_inventories(self, bag_quantities: dict, item_quantities: dict):
         # Update bag inventories
        for bag_id, bag_quantity in bag_quantities.items():
            bag_inventory = await self.inventory_repo.get_by_bag_id(bag_id)
            bag_inventory_dict = asdict(Inventory(**bag_inventory))
            bag_inventory_dict["current_stock"] -= bag_quantity
            await self.inventory_repo.update(bag_inventory.id, bag_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = {
                "inventory_id": bag_inventory.id,
                "transaction_type": "sale",
                "quantity": bag_quantity
            }
            await self.inventory_transactoin_repo.create(inventory_transaction)
        
        # Update item inventories
        for item_id, item_quantity in item_quantities.items():
            item_inventory = await self.inventory_repo.get_by_item_id(item_id)
            item_inventory_dict = asdict(Inventory(**item_inventory))
            item_inventory_dict["current_stock"] -= item_quantity
            await self.inventory_repo.update(item_inventory.id, item_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = {
                "inventory_id": item_inventory.id,
                "transaction_type": "sale",
                "quantity": item_quantity
            }
            await self.inventory_transactoin_repo.create(inventory_transaction)

    async def check_stock_availability(self, bag_quantities, item_quantities):
        inventories = await self.get_inventories()
        bag_inventories = inventories["bag"]
        item_inventories = inventories["item"]
    
        # Check for bag availability
        for bag_id, bag_quantity in bag_quantities.items():
            if bag_id not in bag_inventories or bag_quantity > bag_inventories[bag_id]:
                return False
        
        # Check for items availability
        for item_id, item_quantity in item_quantities.items():
            if item_id not in item_inventories or item_quantity > item_inventories[item_id]:
                return False
        
        return True
