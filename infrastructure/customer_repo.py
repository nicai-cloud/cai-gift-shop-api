from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.customer_model import CustomerModel


class CustomerRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, customer: dict) -> UUID:
        create_customer_stmt = insert(CustomerModel).values(customer)
        customer_entry = await self.session.execute(create_customer_stmt)
        return customer_entry.inserted_primary_key[0]

    async def get_all(self):
        customers_query = select(
            CustomerModel.id,
            CustomerModel.first_name,
            CustomerModel.last_name,
            CustomerModel.mobile,
            CustomerModel.email,
            CustomerModel.address
        ).where(CustomerModel.deleted_at.is_(None))

        result = await self.session.execute(customers_query)
        return result.all()
    
    async def get_by_id(self, customer_id: UUID):
        try:
            customer_query = select(
                CustomerModel.id,
                CustomerModel.first_name,
                CustomerModel.last_name,
                CustomerModel.mobile,
                CustomerModel.email,
                CustomerModel.address
            ).where(and_(CustomerModel.deleted_at.is_(None), CustomerModel.id == customer_id))

            result = await self.session.execute(customer_query)
            return result.one()
        except MultipleResultsFound:
            raise CustomerRepo.MultipleResultsFound
        except NoResultFound:
            raise CustomerRepo.DoesNotExist


def construct_postgres_customer_repo(transactable: PostgresTransactable) -> CustomerRepo:
    return CustomerRepo(transactable.session)
