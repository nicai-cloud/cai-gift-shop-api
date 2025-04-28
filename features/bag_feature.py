import logging

from api.types import Bag
from infrastructure.bag_repo import BagRepo
from infrastructure.work_management import WorkManager
from utils.media import get_full_image_url, get_full_video_url

LOG = logging.getLogger(__name__)


class BagFeature:
    def __init__(self, work_manager: WorkManager):
        self.bag_repo = work_manager.get(BagRepo)
    
    async def get_bags(self) -> list[Bag]:
        try:
            bags = await self.bag_repo.get_all()
            result = []
            for bag in bags:
                result.append(Bag(
                    id=bag.id,
                    image_url=get_full_image_url(bag.image_url),
                    video_url=get_full_video_url(bag.video_url),
                    name=bag.name,
                    description=bag.description,
                    price=bag.price
                ))
            return result
        except Exception as e:
            LOG.exception("Unable to get bags due to unexpected error", exc_info=e)

    async def get_bag_by_id(self, bag_id: int) -> Bag | None:
        try:
            bag = await self.bag_repo.get_by_id(bag_id)
            return Bag(
                id=bag.id,
                image_url=get_full_image_url(bag.image_url),
                video_url=get_full_video_url(bag.video_url),
                name=bag.name,
                description=bag.description,
                price=bag.price
            )
        except BagRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get bag due to unexpected error", exc_info=e)
