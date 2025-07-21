import logging
from uuid import UUID

from api.types import Customer
from infrastructure.customer_repo import CustomerRepo
from infrastructure.async_work_management import AsyncWorkManager
from models.customer_model import CustomerModel

LOG = logging.getLogger(__name__)


def construct_customer(customer: CustomerModel) -> Customer:
    return Customer(
        id=customer.id,
        first_name=customer.first_name,
        last_name=customer.last_name,
        mobile=customer.mobile,
        email=customer.email
    )


class CustomerFeature:
    def __init__(self, work_manager: AsyncWorkManager):
        self.customer_repo = work_manager.get(CustomerRepo)
    
    async def create_customer(self, first_name: str, last_name: str, email: str, mobile: str) -> UUID:
        try:
            customer = CustomerModel()
            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            customer.mobile = mobile
            await self.customer_repo.add(customer)
            return customer.id
        except Exception as e:
            LOG.exception("Unable to create customer due to unexpected error", exc_info=e)

    async def get_customers(self) -> list[Customer]:
        try:
            customers: list[CustomerModel] = await self.customer_repo.get_all()
            return [construct_customer(customer) for customer in customers]
        except Exception as e:
            LOG.exception("Unable to get customers due to unexpected error", exc_info=e)

    async def get_customer_by_id(self, customer_id: UUID) -> Customer | None:
        try:
            customer: CustomerModel = await self.customer_repo.get_by_id(customer_id)
            return construct_customer(customer)
        except CustomerRepo.DoesNotExist:
            return None
        except Exception as e:
            LOG.exception("Unable to get customer due to unexpected error", exc_info=e)
