import logging
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.work_management import WorkManager
from models.types import Preselection

LOG = logging.getLogger(__name__)


class PreselectionFeature:
    def __init__(self, work_manager: WorkManager):
        self.preselection_repo = work_manager.get(PreselectionRepo)
    
    async def get_preselections(self) -> list[Preselection]:
        try:
            return await self.preselection_repo.get_all()
        except Exception as e:
            LOG.exception("Unable to get preselections due to unexpected error", exc_info=e)

    async def get_preselection(self, preselection_id: int) -> Preselection:
        try:
            return await self.preselection_repo.get(preselection_id)
        except Exception as e:
            LOG.exception("Unable to get preselection due to unexpected error", exc_info=e)
