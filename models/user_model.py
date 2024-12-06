from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String

from models.base import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    mobile = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    # address = Column(String, nullable=False)

    created_at = Column(DateTime, default=timezone.utc)
    updated_at = Column(DateTime, default=timezone.utc, onupdate=datetime.now(timezone.utc))
