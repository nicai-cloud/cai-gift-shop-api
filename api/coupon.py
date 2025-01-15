from falcon import HTTP_OK
from datetime import datetime, timezone

from api.base import RequestHandler, route
from features.coupon_feature import CouponFeature
from infrastructure.work_management import WorkManager


class CouponRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.coupon_feature = CouponFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_coupons(self, req, resp):
        resp.media = await self.coupon_feature.get_coupons()
        resp.status = HTTP_OK

    @route.get("/search", auth_exempt=True)
    async def get_coupon_by_code(self, req, resp):
        code = req.params.get('code')
        coupon = await self.coupon_feature.get_coupon_by_code(code)
        if coupon is None or datetime.now(timezone.utc) > coupon.expiry_date or coupon.used:
            resp.media = {"couponCode": code, "isValid": False, "discountPercentage": 0}
        else:
            resp.media = {"couponCode": code, "isValid": True, "discountPercentage": coupon.discount_percentage}
        resp.status = HTTP_OK
