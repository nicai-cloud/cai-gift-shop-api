from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from models.base import Base


class PreselectionModel(Base):
    __tablename__ = "preselection"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_src = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    bag_id = Column(Integer, ForeignKey("bag.id"), nullable=False)
    item_ids = Column(ARRAY(Integer), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
