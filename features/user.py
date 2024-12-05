import logging
from infrastructure.user import UserRepo

LOG = logging.getLogger(__name__)


class User:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo
    
    async def create_user(self, new_user):
        try:
            await self.user_repo.create(new_user)
        except Exception as e:
            LOG.exception("Unable to create user due to unexpected error", exc_info=e)
