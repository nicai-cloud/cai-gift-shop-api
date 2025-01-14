from uuid import UUID
from falcon import HTTP_OK, HTTPNotFound

from api.base import RequestHandler, route
from features.coupon_feature import CouponFeature
from infrastructure.work_management import WorkManager


class CouponRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.coupon_feature = CouponFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_coupons(self, req, resp):
        resp.media = await self.coupon_feature.get_coupons()
        resp.status = HTTP_OK

    @route.get("/{code}", auth_exempt=True)
    async def get_coupon_by_code(self, req, resp, code):
        code = req.params.get('code')
        coupon = await self.coupon_feature.get_coupon_by_code(code)
        if coupon is None:
            raise HTTPNotFound(description="Coupon not found")

        resp.media  = coupon
        resp.status = HTTP_OK
