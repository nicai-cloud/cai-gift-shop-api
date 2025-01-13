from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.shipping_method_model import ShippingMethodModel


class ShippingMethodRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self):
        shipping_methods_query = select(
            ShippingMethodModel.id,
            ShippingMethodModel.name,
            ShippingMethodModel.fee,
            ShippingMethodModel.discount_fee
        ).where(ShippingMethodModel.deleted_at.is_(None))

        result = await self.session.execute(shipping_methods_query)
        return result.all()
    
    async def get_by_id(self, shipping_method_id: int):
        try:
            shipping_method_query = select(
                ShippingMethodModel.id,
                ShippingMethodModel.name,
                ShippingMethodModel.fee,
                ShippingMethodModel.discount_fee
            ).where(and_(ShippingMethodModel.deleted_at.is_(None), ShippingMethodModel.id == shipping_method_id))

            result = await self.session.execute(shipping_method_query)
            return result.one()
        except MultipleResultsFound:
            raise ShippingMethodRepo.MultipleResultsFound
        except NoResultFound:
            raise ShippingMethodRepo.DoesNotExist


def construct_postgres_shipping_method_repo(transactable: PostgresTransactable) -> ShippingMethodRepo:
    return ShippingMethodRepo(transactable.session)
