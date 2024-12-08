import falcon

from api.base import RequestHandler, route
from features.preselection_feature import PreselectionFeature
from infrastructure.work_management import WorkManager


class PreselectionRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.preselection_feature = PreselectionFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_preselections(self, req, resp):
        resp.media = await self.preselection_feature.get_preselections()
        resp.status = falcon.HTTP_OK

    @route.get("/{preselection_id}", auth_exempt=True)
    async def get_preselection(self, req, resp, preselection_id):
        resp.media = await self.preselection_feature.get_preselection(int(preselection_id))
        resp.status = falcon.HTTP_OK
