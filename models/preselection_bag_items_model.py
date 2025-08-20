from sqlalchemy import Column, ForeignKey, Integer, func, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class PreselectionBagItemsModel(Base, SerializerMixin):
    __tablename__ = "preselection_bag_items"
    __table_args__ = (
        PrimaryKeyConstraint('preselection_id', 'bag_id', 'item_id'),
    )

    preselection_id = Column(Integer, ForeignKey("preselection.id"), nullable=False)
    bag_id = Column(Integer, ForeignKey("bag.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
