from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class InventoryModel(Base, SerializerMixin):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    current_stock = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
