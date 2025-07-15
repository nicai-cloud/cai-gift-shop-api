import logging

from infrastructure.bag_repo import BagRepo
from infrastructure.item_repo import ItemRepo
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.async_work_management import AsyncWorkManager
from utils.media import get_full_image_url

LOG = logging.getLogger(__name__)


class ImageFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.bag_repo = work_manager.get(BagRepo)
        self.item_repo = work_manager.get(ItemRepo)
        self.preselection_repo = work_manager.get(PreselectionRepo)
    
    async def get_all_image_urls(self) -> list[str]:
        images = []
        try:
            bags = await self.bag_repo.get_all()
            images.extend(get_full_image_url(bag.image_url) for bag in bags)

            items = await self.item_repo.get_all()
            images.extend(get_full_image_url(item.image_url) for item in items)

            preselections = await self.preselection_repo.get_all()
            images.extend(get_full_image_url(preselection.image_url) for preselection in preselections)

            return images
        except Exception as e:
            LOG.exception("Unable to get all image urls due to unexpected error", exc_info=e)

    async def get_preselection_image_urls(self) -> list[str]:
        images = []
        try:
            preselections = await self.preselection_repo.get_all()
            images.extend(get_full_image_url(preselection.image_url) for preselection in preselections)

            return images
        except Exception as e:
            LOG.exception("Unable to get preselection image urls due to unexpected error", exc_info=e)

    async def get_custom_image_urls(self) -> list[str]:
        images = []
        try:
            bags = await self.bag_repo.get_all()
            images.extend(get_full_image_url(bag.image_url) for bag in bags)

            items = await self.item_repo.get_all()
            images.extend(get_full_image_url(item.image_url) for item in items)

            return images
        except Exception as e:
            LOG.exception("Unable to get custom image urls due to unexpected error", exc_info=e)
