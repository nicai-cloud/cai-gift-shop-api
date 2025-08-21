import uuid
from sqlalchemy import Column, ForeignKey, Integer, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class OrderItemModel(Base, SerializerMixin):
    __tablename__ = "order_item"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    quantity = Column(Integer, nullable=False)

    preselection_id = Column(Integer, ForeignKey("preselection.id"))
    custom_bag_order_item_id = Column(Integer, ForeignKey("custom_bag_order_item.id"))

    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Adding the CheckConstraint
    __table_args__ = (
        CheckConstraint(
            'preselection_id IS NOT NULL OR custom_bag_order_item_id IS NOT NULL',
            name='check_preselection_id_or_custom_bag_order_item_id_not_null'
        ),
    )
