from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_scoped_session

from models.base import BaseRepository
from models.user import UserModel

from .postgres import PostgresTransactable


class UserRepo(BaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def create(self, user):
        user_stmt = insert(UserModel).values(user)
        await self.session.execute(user_stmt)


def construct_postgres_user_repo(transactable: PostgresTransactable) -> UserRepo:
    return UserRepo(transactable.session)
