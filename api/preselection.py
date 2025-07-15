from falcon import HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetPreselectionsResponse, GetPreselectionResponse
from features.preselection_feature import PreselectionFeature
from infrastructure.async_work_management import AsyncWorkManager


class PreselectionRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.preselection_feature = PreselectionFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_preselections(self, req, resp):
        preselections = await self.preselection_feature.get_preselections()
        resp.media = GetPreselectionsResponse(preselections=preselections)
        resp.status = HTTP_OK

    @route.get("/search", auth_exempt=True)
    async def get_preselection_by_name(self, req, resp):
        preselection_name = req.params.get('name')
        preselection = await self.preselection_feature.get_preselection_by_name(preselection_name)
        if preselection is None:
            raise NotFound(detail=f"Preselection with preselection_name {preselection_name} not found.")
    
        resp.media = GetPreselectionResponse(preselection=preselection)
        resp.status = HTTP_OK
