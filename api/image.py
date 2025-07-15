from falcon import HTTP_OK

from api.base import RequestHandler, route
from api.response_types import GetImagesResponse
from features.image_feature import ImageFeature
from infrastructure.async_work_management import AsyncWorkManager


class ImageRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.image_feature = ImageFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_all_image_urls(self, req, resp):
        images = await self.image_feature.get_all_image_urls()
        resp.media = GetImagesResponse(images=images)
        resp.status = HTTP_OK

    @route.get("/preselection", auth_exempt=True)
    async def get_preselection_image_urls(self, req, resp):
        images = await self.image_feature.get_preselection_image_urls()
        resp.media = GetImagesResponse(images=images)
        resp.status = HTTP_OK

    @route.get("/custom", auth_exempt=True)
    async def get_custom_image_urls(self, req, resp):
        images = await self.image_feature.get_custom_image_urls()
        resp.media = GetImagesResponse(images=images)
        resp.status = HTTP_OK
