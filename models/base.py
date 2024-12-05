from sqlalchemy.orm import Query, declarative_base
from sqlalchemy import MetaData, Column, DateTime, select

class NotDeletedQuery(Query):
    def __init__(self, entities, session=None):
        super().__init__(entities, session=session)
        self.filter_by(deleted_at=None)


class BaseModel:
    deleted_at = Column(DateTime, nullable=True)
    query_class = NotDeletedQuery

metadata = MetaData()
Base = declarative_base(metadata=metadata, cls=BaseModel)


class BaseRepository:
    def __init__(self, session):
        self.session = session

    async def get_filtered_query(self, model):
        query = select(model).where(model.deleted_at.is_(None))
        return query
