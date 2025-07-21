from collections import defaultdict
import logging

from api.types import Item
from infrastructure.item_repo import ItemRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.item_model import ItemModel
from utils.media import get_full_image_url, get_full_video_url

LOG = logging.getLogger(__name__)


def construct_item(item: ItemModel) -> Item:
    return Item(
        id=item.id,
        image_url=get_full_image_url(item.image_url),
        video_url=get_full_video_url(item.video_url),
        product=item.product,
        name=item.name,
        description=item.description,
        price=item.price
    )


class ItemFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.item_repo = work_manager.get(ItemRepo)
    
    async def get_items(self) -> list[Item]:
        try:
            items: list[ItemModel] = await self.item_repo.get_all()
            result = []
            for item in items:
                result.append(construct_item(item))
            return result
        except Exception as e:
            LOG.exception("Unable to get items due to unexpected error", exc_info=e)
    
    async def get_items_with_product(self) -> dict[str, list[Item]]:
        try:
            items: list[ItemModel] = await self.item_repo.get_all_with_sorting()
            items_dict = defaultdict(list)
            for item in items:
                item = construct_item(item)
                items_dict[item.product].append(item)
            return dict(items_dict)
        except Exception as e:
            LOG.exception("Unable to get items with product due to unexpected error", exc_info=e)

    async def get_item(self, item_id: int) -> Item | None:
        try:
            item: ItemModel = await self.item_repo.get_by_id(item_id)
            return construct_item(item)
        except ItemRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get item due to unexpected error", exc_info=e)
