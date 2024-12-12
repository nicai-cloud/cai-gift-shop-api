from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class OrderItemModel(Base, SerializerMixin):
    __tablename__ = "order_item"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    quantity = Column(Integer, nullable=False)

    preselection_id = Column(Integer, ForeignKey("preselection.id"))
    bag_id = Column(Integer, ForeignKey("bag.id"))
    item_ids = Column(ARRAY(Integer))

    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)

    order = relationship("OrderModel", back_populates="order_items")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Adding the CheckConstraint
    __table_args__ = (
        CheckConstraint(
            'preselection_id IS NOT NULL OR (bag_id IS NOT NULL AND item_ids IS NOT NULL)',
            name='check_preselection_id_or_bag_id_and_item_ids_not_null'
        ),
    )
