from sqlalchemy import Column, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
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

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
