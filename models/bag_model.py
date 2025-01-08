from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy_serializer import SerializerMixin
from models.base import Base


class BagModel(Base, SerializerMixin):
    __tablename__ = "bag"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_url = Column(String, nullable=False)
    video_url = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
