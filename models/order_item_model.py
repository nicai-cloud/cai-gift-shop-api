from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer, CheckConstraint

from models.base import Base


class OrderItemModel(Base):
    __tablename__ = "order_item"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    preselection_id = Column(Integer, ForeignKey("preselection.id"))
    bag_id = Column(Integer, ForeignKey("bag.id"))
    item_ids = Column(ARRAY(Integer))

    created_at = Column(DateTime, default=timezone.utc)
    updated_at = Column(DateTime, default=timezone.utc, onupdate=datetime.now(timezone.utc))

    # Adding the CheckConstraint
    __table_args__ = (
        CheckConstraint(
            'preselection_id IS NOT NULL OR (bag_id IS NOT NULL AND item_ids IS NOT NULL)',
            name='check_preselection_id_or_bag_id_and_item_ids_not_null'
        ),
    )
