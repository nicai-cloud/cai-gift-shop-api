from functools import wraps
from typing import Type, List
from dataclasses import dataclass


def map_to_dataclass(dataclass_type: Type[dataclass]):
    """
    Decorator to map SQLAlchemy query results to a dataclass.
    :param dataclass_type: The target dataclass type.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> List[dataclass]:
            query_result = await func(*args, **kwargs)
            # Map each query result to the dataclass
            return dataclass_type(**{
                column.name: getattr(query_result, column.name, None)
                for column in query_result.__table__.columns
                if column.name not in ('deleted_at', 'created_at', 'updated_at')
            })
        return wrapper
    return decorator


def map_to_dataclasses(dataclass_type: Type[dataclass]):
    """
    Decorator to map SQLAlchemy query results to a dataclass.
    :param dataclass_type: The target dataclass type.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> List[dataclass]:
            query_results = await func(*args, **kwargs)
            # Map each query result to the dataclass
            return [
                dataclass_type(**{
                    column.name: getattr(result, column.name, None)
                    for column in result.__table__.columns
                    if column.name not in ('deleted_at', 'created_at', 'updated_at')
                })
                for result in query_results
            ]
        return wrapper
    return decorator
