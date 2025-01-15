from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import and_, select, update

from infrastructure.postgres import PostgresTransactable
from models.base import BaseRepository
from models.coupon_model import CouponModel


class CouponRepo(BaseRepository):
    class DoesNotExist(Exception):
        pass

    class MultipleResultsFound(Exception):
        pass

    def __init__(self, session: async_scoped_session):
        self.session = session
    
    async def get_all(self):
        coupons_query = select(
            CouponModel.id,
            CouponModel.code,
            CouponModel.discount_percentage,
            CouponModel.description,
            CouponModel.expiry_date,
            CouponModel.used
        ).where(CouponModel.deleted_at.is_(None))

        result = await self.session.execute(coupons_query)
        return result.all()
    
    async def get_by_code(self, code: str):
        try:
            coupon_query = select(
                CouponModel.id,
                CouponModel.code,
                CouponModel.discount_percentage,
                CouponModel.description,
                CouponModel.expiry_date,
                CouponModel.used
            ).where(and_(CouponModel.deleted_at.is_(None), CouponModel.code == code))

            result = await self.session.execute(coupon_query)
            return result.one()
        except MultipleResultsFound:
            raise CouponRepo.MultipleResultsFound
        except NoResultFound:
            raise CouponRepo.DoesNotExist
    
    async def mark_as_used(self, coupon_id: str):
        stmt = update(CouponModel).where(CouponModel.id == coupon_id).values(used=True)
        await self.session.execute(stmt)


def construct_postgres_coupon_repo(transactable: PostgresTransactable) -> CouponRepo:
    return CouponRepo(transactable.session)
