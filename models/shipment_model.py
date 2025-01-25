import uuid
from sqlalchemy import Column, Float, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class ShipmentModel(Base, SerializerMixin):
    __tablename__ = "shipment"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    volume = Column(Float, nullable=True)
    weight = Column(Float, nullable=False)
    delivery_fee = Column(Numeric(10, 2), nullable=False)
    send_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    receive_date = Column(TIMESTAMP(timezone=True), nullable=True)
    tracking_number = Column(String, nullable=False)

    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
