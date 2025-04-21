from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

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
    
    async def get_all(self):
        query = select(
            FulfillmentMethodModel.id,
            FulfillmentMethodModel.name,
            FulfillmentMethodModel.fee,
            FulfillmentMethodModel.discount_fee
        ).where(FulfillmentMethodModel.deleted_at.is_(None))

        result = await self.session.execute(query)
        return result.all()
    
    async def get_by_id(self, fulfillment_method_id: int):
        try:
            query = select(
                FulfillmentMethodModel.id,
                FulfillmentMethodModel.name,
                FulfillmentMethodModel.fee,
                FulfillmentMethodModel.discount_fee
            ).where(and_(FulfillmentMethodModel.deleted_at.is_(None), FulfillmentMethodModel.id == fulfillment_method_id))

            result = await self.session.execute(query)
            return result.one()
        except MultipleResultsFound:
            raise FulfillmentMethodRepo.MultipleResultsFound
        except NoResultFound:
            raise FulfillmentMethodRepo.DoesNotExist


def construct_postgres_fulfillment_method_repo(transactable: PostgresTransactable) -> FulfillmentMethodRepo:
    return FulfillmentMethodRepo(transactable.session)
