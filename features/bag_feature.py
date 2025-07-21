import logging

from api.types import Bag
from infrastructure.bag_repo import BagRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.bag_model import BagModel
from utils.media import get_full_image_url, get_full_video_url

LOG = logging.getLogger(__name__)


def construct_bag(bag: BagModel) -> Bag:
    return Bag(
        id=bag.id,
        image_url=get_full_image_url(bag.image_url),
        video_url=get_full_video_url(bag.video_url),
        name=bag.name,
        description=bag.description,
        price=bag.price
    )


class BagFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.bag_repo = work_manager.get(BagRepo)
    
    async def get_bags(self) -> list[Bag]:
        try:
            bags: list[BagModel] = await self.bag_repo.get_all()
            result = []
            for bag in bags:
                result.append(construct_bag(bag))
            return result
        except Exception as e:
            LOG.exception("Unable to get bags due to unexpected error", exc_info=e)

    async def get_bag_by_id(self, bag_id: int) -> Bag | None:
        try:
            bag: BagModel = await self.bag_repo.get_by_id(bag_id)
            return construct_bag(bag)
        except BagRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get bag due to unexpected error", exc_info=e)
