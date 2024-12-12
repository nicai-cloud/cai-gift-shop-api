from sqlalchemy.orm import Query, declarative_base
from sqlalchemy import MetaData, Column, DateTime, select

class NotDeletedQuery(Query):
    def __init__(self, entities, session=None):
        super().__init__(entities, session=session)
        self.filter_by(deleted_at=None)


def to_camel_case(snake_str):
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(component.title() for component in components[1:])


class BaseModel:
    deleted_at = Column(DateTime, nullable=True)
    query_class = NotDeletedQuery

    def to_dict(self):
        """
        Convert the SQLAlchemy object into a dictionary
        with camelCase keys.
        """
        result = {}
        for column in self.__table__.columns:
            if column.name not in ('deleted_at', 'created_at', 'updated_at'):
                snake_key = column.name
                camel_key = to_camel_case(snake_key)
                result[camel_key] = getattr(self, snake_key)
        return result


metadata = MetaData()
Base = declarative_base(metadata=metadata, cls=BaseModel)


class BaseRepository:
    def __init__(self, session):
        self.session = session

    async def get_filtered_query(self, model):
        query = select(model).where(model.deleted_at.is_(None))
        return query
