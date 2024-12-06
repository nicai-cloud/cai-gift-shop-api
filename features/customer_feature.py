import logging
from uuid import UUID
from infrastructure.customer import CustomerRepo
from infrastructure.work_management import WorkManager

LOG = logging.getLogger(__name__)


class CustomerFeature:
    def __init__(self, work_manager: WorkManager):
        self.customer_repo = work_manager.get(CustomerRepo)
    
    async def create_customer(self, first_name, last_name, email, mobile, address) -> UUID:
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
