from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.user_model import UserModel


class UserRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, user):
        create_user_stmt = insert(UserModel).values(user)
        await self.session.execute(create_user_stmt)


def construct_postgres_user_repo(transactable: PostgresTransactable) -> UserRepo:
    return UserRepo(transactable.session)
