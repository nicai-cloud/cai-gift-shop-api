import logging
from infrastructure.preselection_repo import PreselectionRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class PreselectionFeature:
    def __init__(self, work_manager: WorkManager):
        self.preselection_repo = work_manager.get(PreselectionRepo)
    
    async def get_preselections(self):
        try:
            return await self.preselection_repo.get_all()
        except Exception as e:
            LOG.exception("Unable to get preselections due to unexpected error", exc_info=e)
