from typing import ClassVar

from dataclasses import field
from marshmallow import Schema
from marshmallow_dataclass import dataclass


class APISchema(Schema):
    pass


@dataclass(base_schema=APISchema)
class CustomerInfoInput:
    first_name: str = field(metadata={"data_key": "firstName"})
    last_name: str = field(metadata={"data_key": "lastName"})
    email: str = field(metadata={"data_key": "email"})
    mobile: str = field(metadata={"data_key": "mobile"})
    address: str = field(metadata={"data_key": "address"})


@dataclass(base_schema=APISchema)
class OrderItemInput:
    quantity: int = field(metadata={"data_key": "quantity"})
    preselection_id: int | None = field(metadata={"data_key": "preselectionId"})
    bag_id: int | None = field(metadata={"data_key": "bagId"})
    item_ids: list[int] | None = field(metadata={"data_key": "itemIds"})


@dataclass(base_schema=APISchema)
class CompleteOrderInput:
    customer_info: CustomerInfoInput = field(metadata={"data_key": "customerInfo"})
    order_items: list[OrderItemInput] = field(metadata={"data_key": "orderItems"})
    shipping_method: int = field(metadata={"data_key": "shippingMethod"})
    coupon_code: str = field(metadata={"data_key": "couponCode"})
    payment_method_id: str = field(metadata={"data_key": "paymentMethodId"})

    Schema: ClassVar[type["Schema"]] = Schema
