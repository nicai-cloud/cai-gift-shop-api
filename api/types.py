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
class BagWithInventory:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    current_stock: int


@dataclass
class Item:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    category: str


@dataclass
class ItemWithInventory:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    category: str
    current_stock: int


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
class Customer:
    id: str
    first_name: str
    last_name: str
    mobile: str
    email: str
    address: str


@dataclass
class Order:
    id: str
    customer_id: str
    amount: float
    order_number: str


@dataclass
class OrderItem:
    id: str
    quantity: int
    preselection_id: int | None
    bag_id: int | None
    item_ids: list[int] | None
    order_id: str


@dataclass
class PublishableKeyResponse:
    publishable_key: str
