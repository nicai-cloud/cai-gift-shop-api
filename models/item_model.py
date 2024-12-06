from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from models.base import Base


class ItemModel(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_src = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
