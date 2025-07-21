from collections import defaultdict
import logging

from api.types import Inventory
from infrastructure.inventory_repo import InventoryRepo
from infrastructure.inventory_transaction_repo import InventoryTransactionRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.inventory_model import InventoryModel
from models.inventory_transaction_model import InventoryTransactionModel
from dataclasses import asdict

LOG = logging.getLogger(__name__)


def construct_inventory(inventory: InventoryModel) -> Inventory:
    return Inventory(
        id=inventory.id,
        entity_type=inventory.entity_type,
        entity_id=inventory.entity_id,
        current_stock=inventory.current_stock,
        low_stock_threshold=inventory.low_stock_threshold
    )


class InventoryFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.inventory_repo = work_manager.get(InventoryRepo)
        self.inventory_transactoin_repo = work_manager.get(InventoryTransactionRepo)
    
    async def get_inventories(self) -> dict[str, dict[str, int]]:
        try:
            inventories: list[InventoryModel] = await self.inventory_repo.get_all()
            inventories_dict = defaultdict(dict[str, int])
            for inventory in inventories:
                inventories_dict[inventory.entity_type].update({str(inventory.entity_id): inventory.current_stock})
            return dict(inventories_dict)
        except Exception as e:
            LOG.exception("Unable to get inventories due to unexpected error", exc_info=e)

    async def get_inventory_by_id(self, inventory_id: int) -> Inventory | None:
        try:
            inventory: InventoryModel = await self.inventory_repo.get_by_id(inventory_id)
            return construct_inventory(inventory)
        except InventoryRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)

    async def get_inventory_by_bag_id(self, bag_id: int) -> Inventory | None:
        try:
            inventory: InventoryModel = await self.inventory_repo.get_by_bag_id(bag_id)
            return construct_inventory(inventory)
        except InventoryRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)

    async def get_inventory_by_item_id(self, item_id: int) -> Inventory | None:
        try:
            inventory: InventoryModel = await self.inventory_repo.get_by_item_id(item_id)
            return construct_inventory(inventory)
        except InventoryRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get inventory due to unexpected error", exc_info=e)
    
    async def refill_bags(self, bag_id: int, quantity: int):
        try:
            bag_inventory: InventoryModel = await self.inventory_repo.get_by_bag_id(bag_id)
            bag_inventory_dict = asdict(construct_inventory(bag_inventory))
            bag_inventory_dict["current_stock"] += quantity
            await self.inventory_repo.update(bag_inventory.id, bag_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = InventoryTransactionModel()
            inventory_transaction.inventory_id = bag_inventory.id
            inventory_transaction.transaction_type = "refill"
            inventory_transaction.quantity = quantity
            await self.inventory_transactoin_repo.add(inventory_transaction)
        except Exception as e:
            LOG.exception("Unable to refill bags due to unexpected error", exc_info=e)
    
    async def refill_items(self, item_id: int, quantity: int):
        try:
            item_inventory: InventoryModel = await self.inventory_repo.get_by_item_id(item_id)
            item_inventory_dict = asdict(construct_inventory(item_inventory))
            item_inventory_dict["current_stock"] += quantity
            await self.inventory_repo.update(item_inventory.id, item_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = InventoryTransactionModel()
            inventory_transaction.inventory_id = item_inventory.id
            inventory_transaction.transaction_type = "refill"
            inventory_transaction.quantity = quantity
            await self.inventory_transactoin_repo.add(inventory_transaction)
        except Exception as e:
            LOG.exception("Unable to refill items due to unexpected error", exc_info=e)
    
    async def update_inventories(self, bag_quantities: dict, item_quantities: dict):
         # Update bag inventories
        for bag_id, bag_quantity in bag_quantities.items():
            bag_inventory: InventoryModel = await self.inventory_repo.get_by_bag_id(bag_id)
            bag_inventory_dict = asdict(construct_inventory(bag_inventory))
            bag_inventory_dict["current_stock"] -= bag_quantity
            await self.inventory_repo.update(bag_inventory.id, bag_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = InventoryTransactionModel()
            inventory_transaction.inventory_id = bag_inventory.id
            inventory_transaction.transaction_type = "sale"
            inventory_transaction.quantity = bag_quantity
            await self.inventory_transactoin_repo.add(inventory_transaction)
        
        # Update item inventories
        for item_id, item_quantity in item_quantities.items():
            item_inventory: InventoryModel = await self.inventory_repo.get_by_item_id(item_id)
            item_inventory_dict = asdict(construct_inventory(item_inventory))
            item_inventory_dict["current_stock"] -= item_quantity
            await self.inventory_repo.update(item_inventory.id, item_inventory_dict)

            # Also create inventory_transaction record
            inventory_transaction = InventoryTransactionModel()
            inventory_transaction.inventory_id = item_inventory.id
            inventory_transaction.transaction_type = "sale"
            inventory_transaction.quantity = item_quantity
            await self.inventory_transactoin_repo.add(inventory_transaction)

    async def check_stock_availability(self, ordered_bag_quantities, ordered_item_quantities):
        try:
            inventories = await self.get_inventories()
            bag_inventories = inventories["bag"]
            item_inventories = inventories["item"]

            bag_id_inventories = {int(bag_id): stock for bag_id, stock in bag_inventories.items()}
            item_id_inventories = {int(item_id): stock for item_id, stock in item_inventories.items()}
        
            # Check for bag availability
            for ordered_bag_id, ordered_bag_quantity in ordered_bag_quantities.items():
                if ordered_bag_id not in bag_id_inventories or ordered_bag_quantity > bag_id_inventories[ordered_bag_id]:
                    return False
            
            # Check for items availability
            for ordered_item_id, ordered_item_quantity in ordered_item_quantities.items():
                if ordered_item_id not in item_id_inventories or ordered_item_quantity > item_id_inventories[ordered_item_id]:
                    return False
            
            return True
        except Exception:
            return False
