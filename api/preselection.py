from falcon import HTTP_OK, HTTPNotFound

from api.base import RequestHandler, route
from features.preselection_feature import PreselectionFeature
from infrastructure.work_management import WorkManager


class PreselectionRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.preselection_feature = PreselectionFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_preselections(self, req, resp):
        resp.media = await self.preselection_feature.get_preselections()
        resp.status = HTTP_OK

    @route.get("/search", auth_exempt=True)
    async def get_preselection_by_name(self, req, resp):
        preselection_name = req.params.get('name')
        preselection = await self.preselection_feature.get_preselection_by_name(preselection_name)
        if preselection is None:
            raise HTTPNotFound(description="Preselection not found")
    
        resp.media = preselection
        resp.status = HTTP_OK
