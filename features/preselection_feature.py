import logging

from api.types import Preselection
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.async_work_management import AsyncWorkManager
from utils.media import get_full_image_url, get_full_video_url

LOG = logging.getLogger(__name__)


class PreselectionFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.preselection_repo = work_manager.get(PreselectionRepo)
    
    async def get_preselections(self) -> list[Preselection]:
        try:
            preselections = await self.preselection_repo.get_all()
            result = []
            for preselection in preselections:
                result.append(Preselection(
                    id=preselection.id,
                    image_url=get_full_image_url(preselection.image_url),
                    video_url=get_full_video_url(preselection.video_url),
                    name=preselection.name,
                    gender=preselection.gender,
                    description=preselection.description,
                    price=preselection.price,
                    bag_id=preselection.bag_id,
                    item_ids=preselection.item_ids
                ))
            return result
        except Exception as e:
            LOG.exception("Unable to get preselections due to unexpected error", exc_info=e)

    async def get_preselection_by_name(self, preselection_name: str) -> Preselection | None:
        try:
            preselection = await self.preselection_repo.get_by_name(preselection_name)
            return Preselection(
                id=preselection.id,
                image_url=get_full_image_url(preselection.image_url),
                video_url=get_full_video_url(preselection.video_url),
                name=preselection.name,
                gender=preselection.gender,
                description=preselection.description,
                price=preselection.price,
                bag_id=preselection.bag_id,
                item_ids=preselection.item_ids
            )
        except PreselectionRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get preselection due to unexpected error", exc_info=e)
