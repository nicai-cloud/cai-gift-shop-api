from datetime import datetime, UTC
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy_serializer import SerializerMixin

from models.base import Base


class CustomerModel(Base, SerializerMixin):
    __tablename__ = "customer"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
