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


def construct_postgres_customer_repo(transactable: PostgresTransactable) -> CustomerRepo:
    return CustomerRepo(transactable.session)
