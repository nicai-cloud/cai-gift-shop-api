from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class InventoryModel(Base, SerializerMixin):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    current_stock = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
