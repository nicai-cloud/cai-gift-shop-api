from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Preselection:
    id: int
    image_url: str
    video_url: str
    name: str
    gender: str
    description: str
    price: Decimal
    bag_id: int
    item_ids: list[int]


@dataclass
class Bag:
    id: int
    image_url: str
    video_url: str
    name: str
    description: str
    price: Decimal


@dataclass
class Item:
    id: int
    image_url: str
    video_url: str
    product: str
    name: str
    description: str
    price: Decimal


@dataclass
class Inventory:
    id: int
    entity_type: str
    entity_id: int
    current_stock: int
    low_stock_threshold: int | None


@dataclass
class Shipment:
    id: str
    volume: float | None
    weight: float
    delivery_fee: Decimal
    send_date: date
    receive_date: date | None
    tracking_number: str
    order_id: str


@dataclass
class ShippingMethod:
    id: int
    name: str
    fee: Decimal
    discount_fee: Decimal


@dataclass
class Coupon:
    id: str
    code: str
    discount_percentage: int
    description: str
    expiry_date: date
    used: bool


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
    subtotal: Decimal
    discount: Decimal
    subtotal_after_discount: Decimal
    shipping_cost: Decimal
    order_number: str
    shipping_method: int
    coupon_id: str | None


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
