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

    @route.get("/id/{preselection_id}", auth_exempt=True)
    async def get_preselection_by_id(self, req, resp, preselection_id):
        resp.media = await self.preselection_feature.get_preselection_by_id(int(preselection_id))
        resp.status = falcon.HTTP_OK

    @route.get("/{preselection_name}", auth_exempt=True)
    async def get_preselection_by_name(self, req, resp, preselection_name):
        resp.media = await self.preselection_feature.get_preselection_by_name(preselection_name)
        resp.status = falcon.HTTP_OK
