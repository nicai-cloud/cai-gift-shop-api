from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey

from models.base import Base


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    order_timestamp = Column(DateTime, nullable=False)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey("order_item.id"), nullable=False)

    created_at = Column(DateTime, default=timezone.utc)
    updated_at = Column(DateTime, default=timezone.utc, onupdate=datetime.now(timezone.utc))
