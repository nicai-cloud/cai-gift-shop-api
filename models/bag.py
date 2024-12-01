from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from models.base import Base


class BagModel(Base):
    __tablename__ = "bag"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.timezone.utc)
    updated_at = Column(DateTime, default=datetime.timezone.utc, onupdate=datetime.now(timezone.utc))
