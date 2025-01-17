from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class CouponModel(Base, SerializerMixin):
    __tablename__ = "coupon"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, server_default=func.gen_random_uuid())
    code = Column(String, nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    expiry_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    used = Column(Boolean, nullable=False, server_default='false')

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
