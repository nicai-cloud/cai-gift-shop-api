from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.fulfillment_method_model import FulfillmentMethodModel


class FulfillmentMethodRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self) -> list[FulfillmentMethodModel]:
        query = await self.get_filtered_query(FulfillmentMethodModel)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, fulfillment_method_id: int) -> FulfillmentMethodModel:
        try:
            query = await self.get_filtered_query(FulfillmentMethodModel)
            query = query.where(FulfillmentMethodModel.id == fulfillment_method_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except MultipleResultsFound:
            raise FulfillmentMethodRepo.MultipleResultsFound
        except NoResultFound:
            raise FulfillmentMethodRepo.DoesNotExist


def construct_postgres_fulfillment_method_repo(transactable: PostgresTransactable) -> FulfillmentMethodRepo:
    return FulfillmentMethodRepo(transactable.session)
