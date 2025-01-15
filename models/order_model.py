import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String, func
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class OrderModel(Base, SerializerMixin):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)
    subtotal_after_discount = Column(Float, nullable=True)
    shipping_cost = Column(Float, nullable=False)
    order_number = Column(String, nullable=False)
    shipping_method = Column(Integer, ForeignKey("shipping_method.id"), nullable=False)
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("coupon.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_order_number_unique_if_not_deleted", "order_number", unique=True, postgresql_where=(deleted_at is None)),
    )