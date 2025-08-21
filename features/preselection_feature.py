import logging

from api.types import Preselection
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.preselection_bag_items_repo import PreselectionBagItemsRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.preselection_model import PreselectionModel
from models.preselection_bag_items_model import PreselectionBagItemsModel
from utils.media import get_full_image_url, get_full_video_url

LOG = logging.getLogger(__name__)


def construct_preselection(preselection: PreselectionModel, preselection_bag_items: list[PreselectionBagItemsModel]) -> Preselection:
    return Preselection(
        id=preselection.id,
        image_url=get_full_image_url(preselection.image_url),
        video_url=get_full_video_url(preselection.video_url),
        name=preselection.name,
        gender=preselection.gender,
        description=preselection.description,
        price=preselection.price,
        bag_id=preselection_bag_items[0].bag_id,
        item_ids=[pbi.item_id for pbi in preselection_bag_items]
    )


class PreselectionFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.preselection_repo = work_manager.get(PreselectionRepo)
        self.preselection_bag_items_repo = work_manager.get(PreselectionBagItemsRepo)
    
    async def get_preselections(self) -> list[Preselection]:
        try:
            preselections: list[PreselectionModel] = await self.preselection_repo.get_all()
            result = []
            for preselection in preselections:
                preselection_bag_items: list[PreselectionBagItemsModel] = await self.preselection_bag_items_repo.get_by_preselection_id(preselection.id)
                result.append(construct_preselection(preselection, preselection_bag_items))
            return result
        except Exception as e:
            LOG.exception("Unable to get preselections due to unexpected error", exc_info=e)

    async def get_preselection_by_name(self, preselection_name: str) -> Preselection | None:
        try:
            preselection: PreselectionModel = await self.preselection_repo.get_by_name(preselection_name)
            preselection_bag_items: list[PreselectionBagItemsModel] = await self.preselection_bag_items_repo.get_by_preselection_id(preselection.id)
            return construct_preselection(preselection, preselection_bag_items)
        except PreselectionRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get preselection due to unexpected error", exc_info=e)
