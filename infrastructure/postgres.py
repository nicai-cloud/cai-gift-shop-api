import logging

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from .work_management import Transactable, current_request_task

LOG = logging.getLogger(__name__)


metadata = MetaData()


class PostgresTransactable(Transactable):
    def __init__(
        self,
        database_url: str,
        session_class: async_scoped_session | None = None,
        log_database_queries: bool = False,
    ):
        if session_class is not None:
            self.session = session_class
        else:
            engine = create_async_engine(
                database_url,
                echo=log_database_queries,
                pool_recycle=3600,
                pool_size=10,
                max_overflow=20,
            )
            self.session = async_scoped_session(
                sessionmaker(engine, class_=AsyncSession),
                scopefunc=current_request_task.get,
            )

    async def begin(self):
        LOG.debug("Now calling begin.")
        return

    async def rollback(self):
        LOG.debug("Calling proper rollback.")
        await self.session.rollback()

    async def commit(self):
        LOG.debug("Calling proper commit.")
        await self.session.commit()

    async def close(self):
        LOG.debug("Calling close.")
        await self.session.close()

    async def begin_nested(self):
        LOG.debug("Beginning nested.")
        self.session.begin_nested()

    async def rollback_nested(self):
        LOG.debug("Rolling back nested.")
        self.session.rollback()

    async def commit_nested(self):
        LOG.debug("Committing nested.")
        await self.session.commit()
