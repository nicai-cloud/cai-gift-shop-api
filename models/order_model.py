from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Column, DateTime, Float, ForeignKey

from models.base import Base


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    order_item_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    amount = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
