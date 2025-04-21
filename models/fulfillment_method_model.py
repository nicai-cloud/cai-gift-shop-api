from sqlalchemy import Column, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class FulfillmentMethodModel(Base, SerializerMixin):
    __tablename__ = "fulfillment_method"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    fee = Column(Numeric(10, 2), nullable=False)
    discount_fee = Column(Numeric(10, 2), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
