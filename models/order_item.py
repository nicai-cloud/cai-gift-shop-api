from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from models.base import Base


class OrderItemModel(Base):
    __tablename__ = "order_item"

    suid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    bag_id = Column(Integer, ForeignKey("bag.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)

    created_at = Column(DateTime, default=timezone.utc)
    updated_at = Column(DateTime, default=timezone.utc, onupdate=datetime.now(timezone.utc))
