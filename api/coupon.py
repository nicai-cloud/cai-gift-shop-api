from falcon import HTTP_OK
from datetime import datetime, timezone

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetCouponsResponse, GetCouponResponse
from features.coupon_feature import CouponFeature
from infrastructure.async_work_management import AsyncWorkManager


class CouponRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.coupon_feature = CouponFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_coupons(self, req, resp):
        coupons = await self.coupon_feature.get_coupons()
        resp.media = GetCouponsResponse(coupons=coupons)
        resp.status = HTTP_OK

    @route.get("/search", auth_exempt=True)
    async def get_coupon_by_code(self, req, resp):
        code = req.params.get('code')
        coupon = await self.coupon_feature.get_coupon_by_code(code)
        if coupon is None:
            raise NotFound(detail=f"Coupon with code {code} not found.")
        
        if datetime.now(timezone.utc) > coupon.expiry_date or coupon.used:
            resp.media = GetCouponResponse(coupon_code=code, is_valid=False, discount_percentage=0)
        else:
            resp.media = GetCouponResponse(coupon_code=code, is_valid=True, discount_percentage=coupon.discount_percentage)
        resp.status = HTTP_OK
