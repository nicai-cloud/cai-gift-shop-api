from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from models.base import Base


class ItemModel(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)

    created_at = Column(DateTime, default=timezone.utc)
    updated_at = Column(DateTime, default=timezone.utc, onupdate=datetime.now(timezone.utc))
