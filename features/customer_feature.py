import logging
from uuid import UUID

from api.types import Customer
from infrastructure.customer_repo import CustomerRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class CustomerFeature:
    def __init__(self, work_manager: WorkManager):
        self.customer_repo = work_manager.get(CustomerRepo)
    
    async def create_customer(self, first_name: str, last_name: str, email: str, mobile: str, address: str) -> UUID:
        try:
            customer = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "mobile": mobile,
                "address": address
            }
            return await self.customer_repo.create(customer)
        except Exception as e:
            LOG.exception("Unable to create customer due to unexpected error", exc_info=e)

    async def get_customers(self) -> list[Customer]:
        try:
            customers = await self.customer_repo.get_all()
            return [Customer(**customer) for customer in customers]
        except Exception as e:
            LOG.exception("Unable to get customers due to unexpected error", exc_info=e)

    async def get_customer_by_id(self, customer_id: UUID) -> Customer | None:
        try:
            customer = await self.customer_repo.get_by_id(customer_id)
            return Customer(**customer)
        except CustomerRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get customer due to unexpected error", exc_info=e)
