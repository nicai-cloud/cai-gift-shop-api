from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.item_model import ItemModel


class ItemRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def get_all(self):
        items_query = select(
            ItemModel.id,
            ItemModel.image_url,
            ItemModel.video_url,
            ItemModel.product,
            ItemModel.name,
            ItemModel.description,
            ItemModel.price
        ).where(ItemModel.deleted_at.is_(None))

        result = await self.session.execute(items_query)
        return result.all()
    
    async def get_all_with_sorting(self):
        items_with_sorting = select(
            ItemModel.id,
            ItemModel.image_url,
            ItemModel.video_url,
            ItemModel.product,
            ItemModel.name,
            ItemModel.description,
            ItemModel.price
        ).where(ItemModel.deleted_at.is_(None)).order_by(ItemModel.product, ItemModel.name)

        result = await self.session.execute(items_with_sorting)
        return result.all()

    async def get_by_id(self, item_id: int):
        item_query = select(
            ItemModel.id,
            ItemModel.image_url,
            ItemModel.video_url,
            ItemModel.product,
            ItemModel.name,
            ItemModel.description,
            ItemModel.price
        ).where(and_(ItemModel.deleted_at.is_(None), ItemModel.id == item_id))

        result = await self.session.execute(item_query)    
        return result.first()


def construct_postgres_item_repo(transactable: PostgresTransactable) -> ItemRepo:
    return ItemRepo(transactable.session)
