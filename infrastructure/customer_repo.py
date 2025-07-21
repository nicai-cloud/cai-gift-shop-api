from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

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

    async def add(self, customer: CustomerModel):
        self.session.add(customer)
        await self.session.flush()

    async def get_all(self) -> list[CustomerModel]:
        query = await self.get_filtered_query(CustomerModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, customer_id: UUID) -> CustomerModel:
        try:
            query = await self.get_filtered_query(CustomerModel)
            query = query.where(CustomerModel.id == customer_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise CustomerRepo.MultipleResultsFound
        except NoResultFound:
            raise CustomerRepo.DoesNotExist


def construct_postgres_customer_repo(transactable: PostgresTransactable) -> CustomerRepo:
    return CustomerRepo(transactable.session)
