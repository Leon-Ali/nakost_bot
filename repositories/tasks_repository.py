from datetime import datetime

from settings import TodoServiceConfig

from .base_repository import BaseRepository
from constants import HTTP


class TasksRepository(BaseRepository):

    async def create_task(
            self,
            user_id: str,
            description: str,
            date: datetime.date,
    ):
        url = TodoServiceConfig.get_task_create_url()
        data = {
            'user': user_id,
            'description': description,
            'date': str(date),
        }
        await self.request(url=url, data=data, method=HTTP.POST)

    async def get_tasks(
            self,
            user_id: str,
            date: datetime.date,
    ):
        url = TodoServiceConfig.get_task_create_url()
        query_params = {
            'user': user_id,
            'date': str(date),
        }
        response = await self.request(url=url, params=query_params)
        return response

