from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class OrderModel(Base, SerializerMixin):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    amount = Column(Float, nullable=False)
    order_number = Column(String, nullable=False)

    order_items = relationship("OrderItemModel", back_populates="order")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
