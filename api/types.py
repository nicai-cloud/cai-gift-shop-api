from dataclasses import dataclass


@dataclass
class Preselection:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    bag_id: int
    item_ids: list[int]


@dataclass
class Bag:
    id: int
    image_url: str
    name: str
    description: str
    price: float


@dataclass
class Item:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    category: str


@dataclass
class Inventory:
    id: int
    entity_type: str
    entity_id: int
    current_stock: int
    low_stock_threshold: int | None


@dataclass
class InventoryTransaction:
    id: str
    inventory_id: int
    transaction_type: str
    quantity: int


@dataclass
class PublishableKeyResponse:
    publishable_key: str
