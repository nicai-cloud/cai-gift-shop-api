import falcon

from api.base import RequestHandler, route
from features.promo_code_feature import PromoCodeFeature
from infrastructure.work_management import WorkManager


class PromoCodeRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.promo_code_feature = PromoCodeFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_promo_codes(self, req, resp):
        resp.media = await self.promo_code_feature.get_promo_codes()
        resp.status = falcon.HTTP_OK

    @route.get("/{promo_code_id}", auth_exempt=True)
    async def get_promo_code(self, req, resp, promo_code_id):
        resp.media = await self.promo_code_feature.get_promo_code(int(promo_code_id))
        resp.status = falcon.HTTP_OK
