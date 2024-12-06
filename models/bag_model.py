from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from models.base import Base


class BagModel(Base):
    __tablename__ = "bag"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_src = Column(String, nullable=False)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
