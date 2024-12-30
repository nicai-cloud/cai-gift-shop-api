from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.customer_model import CustomerModel


class CustomerRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, customer: dict) -> UUID:
        create_customer_stmt = insert(CustomerModel).values(customer)
        customer_entry = await self.session.execute(create_customer_stmt)
        return customer_entry.inserted_primary_key[0]

    async def get_all(self):
        customers_query = await self.get_filtered_query(CustomerModel)
        result = await self.session.execute(customers_query)
        
        return result.scalars().all()
    
    async def get_by_id(self, customer_id: str):
        customer_query = await self.get_filtered_query(CustomerModel)
        result = await self.session.execute(customer_query.where(CustomerModel.id == customer_id))
            
        customer = result.scalars().first()
        return customer


def construct_postgres_customer_repo(transactable: PostgresTransactable) -> CustomerRepo:
    return CustomerRepo(transactable.session)
