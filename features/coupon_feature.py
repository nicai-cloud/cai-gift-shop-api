import logging

from api.types import Coupon
from infrastructure.coupon_repo import CouponRepo
from infrastructure.async_work_management import AsyncWorkManager

LOG = logging.getLogger(__name__)


class CouponFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.coupon_repo = work_manager.get(CouponRepo)
    
    async def get_coupons(self) -> list[Coupon]:
        try:
            coupons = await self.coupon_repo.get_all()
            return [Coupon(**coupon) for coupon in coupons]
        except Exception as e:
            LOG.exception("Unable to get coupons due to unexpected error", exc_info=e)

    async def get_coupon_by_code(self, code: str) -> Coupon | None:
        try:
            coupon = await self.coupon_repo.get_by_code(code)
            return Coupon(**coupon)
        except CouponRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get coupon due to unexpected error", exc_info=e)

    async def mark_as_used(self, coupon: Coupon):
        await self.coupon_repo.mark_as_used(coupon.id)
