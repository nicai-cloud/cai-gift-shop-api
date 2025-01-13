import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class InventoryTransactionModel(Base, SerializerMixin):
    __tablename__ = "inventory_transaction"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
