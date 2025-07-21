import logging

from api.types import Coupon
from infrastructure.coupon_repo import CouponRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.coupon_model import CouponModel

LOG = logging.getLogger(__name__)


def construct_coupon(coupon: CouponModel) -> Coupon:
    return Coupon(
        id=coupon.id,
        code=coupon.code,
        discount_percentage=coupon.discount_percentage,
        description=coupon.description,
        expiry_date=coupon.expiry_date,
        used=coupon.used
    )


class CouponFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.coupon_repo = work_manager.get(CouponRepo)
    
    async def get_coupons(self) -> list[Coupon]:
        try:
            coupons: list[CouponModel] = await self.coupon_repo.get_all()
            return [construct_coupon(coupon) for coupon in coupons]
        except Exception as e:
            LOG.exception("Unable to get coupons due to unexpected error", exc_info=e)

    async def get_coupon_by_code(self, code: str) -> Coupon | None:
        try:
            coupon: CouponModel = await self.coupon_repo.get_by_code(code)
            return construct_coupon(coupon)
        except CouponRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get coupon due to unexpected error", exc_info=e)

    async def mark_as_used(self, coupon: Coupon):
        await self.coupon_repo.mark_as_used(coupon.id)
