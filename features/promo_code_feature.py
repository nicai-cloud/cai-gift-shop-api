import logging
from uuid import UUID

from api.types import PromoCode
from infrastructure.promo_code_repo import PromoCodeRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class PromoCodeFeature:
    def __init__(self, work_manager: WorkManager):
        self.promo_code_repo = work_manager.get(PromoCodeRepo)
    
    async def get_promo_codes(self) -> list[PromoCode]:
        try:
            promo_codes = await self.promo_code_repo.get_all()
            return [PromoCode(**promo_code) for promo_code in promo_codes]
        except Exception as e:
            LOG.exception("Unable to get promo codes due to unexpected error", exc_info=e)

    async def get_promo_code(self, promo_code_id: UUID) -> PromoCode:
        try:
            promo_code = await self.promo_code_repo.get_by_id(promo_code_id)
            return PromoCode(**promo_code)
        except PromoCodeRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get promo code due to unexpected error", exc_info=e)
