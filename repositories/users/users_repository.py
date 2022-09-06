from settings import TodoServiceConfig

from repositories.base_repository import BaseRepository
from .abstract_repository import AbstractUserRepository
from constants import HTTP


class UsersRepository(AbstractUserRepository, BaseRepository):

    async def create_user(self, user_id: str):
        url = TodoServiceConfig.get_user_create_url()
        data = {'user_id': user_id}
        await self.request(url=url, data=data, method=HTTP.POST)
