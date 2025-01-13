from uuid import UUID
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.promo_code_model import PromoCodeModel


class PromoCodeRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self):
        promo_codes_query = select(
            PromoCodeModel.id,
            PromoCodeModel.code,
            PromoCodeModel.discount_percentage,
            PromoCodeModel.description,
            PromoCodeModel.expiry_date,
            PromoCodeModel.expired,
            PromoCodeModel.used
        ).where(PromoCodeModel.deleted_at.is_(None))

        result = await self.session.execute(promo_codes_query)
        return result.all()
    
    async def get_by_id(self, promo_code_id: UUID):
        try:
            promo_code_query = select(
                PromoCodeModel.id,
                PromoCodeModel.code,
                PromoCodeModel.discount_percentage,
                PromoCodeModel.description,
                PromoCodeModel.expiry_date,
                PromoCodeModel.expired,
                PromoCodeModel.used
            ).where(and_(PromoCodeModel.deleted_at.is_(None), PromoCodeModel.id == promo_code_id))

            result = await self.session.execute(promo_code_query)
            return result.one()
        except MultipleResultsFound:
            raise PromoCodeRepo.MultipleResultsFound
        except NoResultFound:
            raise PromoCodeRepo.DoesNotExist


def construct_postgres_promo_code_repo(transactable: PostgresTransactable) -> PromoCodeRepo:
    return PromoCodeRepo(transactable.session)
