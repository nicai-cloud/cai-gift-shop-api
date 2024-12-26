import logging

from api.types import Preselection
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class PreselectionFeature:
    def __init__(self, work_manager: WorkManager):
        self.preselection_repo = work_manager.get(PreselectionRepo)
    
    async def get_preselections(self) -> list[Preselection]:
        try:
            preselections = await self.preselection_repo.get_all()
            return [Preselection(**preselection.to_dict()) for preselection in preselections]
        except Exception as e:
            LOG.exception("Unable to get preselections due to unexpected error", exc_info=e)

    async def get_preselection_by_id(self, preselection_id: int) -> Preselection:
        try:
            preselection = await self.preselection_repo.get_by_id(preselection_id)
            return Preselection(**preselection.to_dict())
        except Exception as e:
            LOG.exception("Unable to get preselection due to unexpected error", exc_info=e)

    async def get_preselection_by_name(self, preselection_name: str) -> Preselection:
        try:
            preselection = await self.preselection_repo.get_by_name(preselection_name)
            return Preselection(**preselection.to_dict())
        except Exception as e:
            LOG.exception("Unable to get preselection due to unexpected error", exc_info=e)
