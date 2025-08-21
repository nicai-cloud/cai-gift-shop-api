from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class CustomBagItemsModel(Base, SerializerMixin):
    __tablename__ = "custom_bag_items"
    __table_args__ = (
        PrimaryKeyConstraint('custom_bag_order_item_id', 'bag_id', 'item_id'),
    )

    custom_bag_order_item_id = Column(Integer, ForeignKey("custom_bag_order_item.id"), nullable=False)
    bag_id = Column(Integer, ForeignKey("bag.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())