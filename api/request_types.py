from dataclasses import field
from decimal import Decimal
from marshmallow import Schema, validate
from marshmallow_dataclass import dataclass


class APISchema(Schema):
    pass


@dataclass(base_schema=APISchema)
class CustomerInfoRequest:
    first_name: str = field(metadata={"data_key": "firstName"})
    last_name: str = field(metadata={"data_key": "lastName"})
    email: str = field(metadata={"validate": validate.Email(error="Invalid email address")})
    mobile: str


@dataclass(base_schema=APISchema)
class OrderItemRequets:
    quantity: int
    preselection_id: int | None = field(metadata={"data_key": "preselectionId"})
    bag_id: int | None = field(metadata={"data_key": "bagId"})
    item_ids: list[int] | None = field(metadata={"data_key": "itemIds"})


@dataclass(base_schema=APISchema)
class CompleteOrderRequest:
    customer_info: CustomerInfoRequest = field(metadata={"data_key": "customerInfo"})
    order_items: list[OrderItemRequets] = field(metadata={"data_key": "orderItems"})
    fulfillment_method: int = field(metadata={"data_key": "fulfillmentMethod"})
    delivery_address: str | None = field(metadata={"data_key": "deliveryAddress"})
    coupon_code: str | None = field(metadata={"data_key": "couponCode"})
    payment_method_id: str = field(metadata={"data_key": "paymentMethodId"})


@dataclass(base_schema=APISchema)
class OrderItemsRequest:
    order_items: list[OrderItemRequets] = field(metadata={"data_key": "orderItems"})


@dataclass(base_schema=APISchema)
class RefillBagRequest:
    bag_id: int = field(metadata={"data_key": "bagId"})
    quantity: int


@dataclass(base_schema=APISchema)
class RefillItemRequest:
    item_id: int = field(metadata={"data_key": "itemId"})
    quantity: int


@dataclass(base_schema=APISchema)
class CreateShipmentRequest:
    volume: float | None
    weight: float
    delivery_fee: Decimal = field(metadata={"data_key": "deliveryFee"})
    tracking_number: str = field(metadata={"data_key": "trackingNumber"})
    order_id: str = field(metadata={"data_key": "orderId"})
