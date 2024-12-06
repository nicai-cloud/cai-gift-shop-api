import logging
from infrastructure.customer import CustomerRepo

LOG = logging.getLogger(__name__)


class CustomerFeature:
    def __init__(self, customer_repo: CustomerRepo):
        self.customer_repo = customer_repo
    
    async def create_customer(self, new_customer):
        try:
            await self.customer_repo.create(new_customer)
        except Exception as e:
            LOG.exception("Unable to create customer due to unexpected error", exc_info=e)
