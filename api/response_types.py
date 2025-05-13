from dataclasses import dataclass
from decimal import Decimal
from api.types import Bag, Coupon, Customer, FulfillmentMethod, Inventory, InventoryTransaction, Item, Order, OrderItem, Preselection, Shipment


@dataclass
class HealthcheckResponse:
    message: str


@dataclass
class GetImagesResponse:
    images: list[str]


@dataclass
class GetCustomersResponse:
    customers: list[Customer]


@dataclass
class GetCustomerResponse:
    customer: Customer


@dataclass
class GetBagsResponse:
    bags: list[Bag]


@dataclass
class GetBagResponse:
    bag: Bag


@dataclass
class GetItemsResponse:
    items: list[Item]


@dataclass
class GetItemResponse:
    item: Item


@dataclass
class GetItemsWithProductResponse:
    items_with_product: dict[str, list[Item]]


@dataclass
class GetPreselectionsResponse:
    preselections: list[Preselection]


@dataclass
class GetPreselectionResponse:
    preselection: Preselection


@dataclass
class GetOrdersResponse:
    orders: list[Order]


@dataclass
class GetOrderResponse:
    order: Order


@dataclass
class GetOrderItemsResponse:
    order_items: list[OrderItem]


@dataclass
class GetOrderItemResponse:
    order_item: OrderItem


@dataclass
class GetInventoriesResponse:
    inventories: list[Inventory]


@dataclass
class GetInventoryResponse:
    inventory: Inventory


@dataclass
class GetInventoryTransactionsResponse:
    inventory_transactions: list[InventoryTransaction]


@dataclass
class GetInventoryTransactionResponse:
    inventory_transaction: InventoryTransaction


@dataclass
class GetFulfillmentMethodsResponse:
    fulfillment_methods: list[FulfillmentMethod]
    free_shipping_threshold: int


@dataclass
class GetFulfillmentMethodResponse:
    fulfillment_method: FulfillmentMethod


@dataclass
class CreateShipmentResponse:
    shipment_id: str


@dataclass
class GetShipmentsResponse:
    shipments: list[Shipment]


@dataclass
class GetShipmentResponse:
    shipment: Shipment


@dataclass
class GetCouponsResponse:
    coupons: list[Coupon]


@dataclass
class GetCouponResponse:
    coupon_code: str
    is_valid: bool
    discount_percentage: int


@dataclass
class CompleteOrderResponse:
    order_number: str


@dataclass
class CalculateSubtotalResponse:
    subtotal: Decimal
    subtotal_after_discount: Decimal


@dataclass
class GetAddressSuggestionsResponse:
    addresses: list[str]


@dataclass
class GetPublishableKeyResponse:
    publishable_key: str
