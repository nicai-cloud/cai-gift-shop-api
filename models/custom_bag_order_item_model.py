from sqlalchemy import Column, Integer, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class CustomBagOrderItemModel(Base, SerializerMixin):
    __tablename__ = "custom_bag_order_item"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())