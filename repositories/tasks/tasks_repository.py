from datetime import datetime
from typing import List

from settings import TodoServiceConfig

from repositories.base_repository import BaseRepository
from constants import HTTP

from .abstract_repository import AbstractTasksRepository


class TasksRepository(AbstractTasksRepository, BaseRepository):

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
            completed=False,
    ):
        url = TodoServiceConfig.get_task_create_url()
        query_params = {
            'user': user_id,
            'date': str(date),
            'finished': str(completed),

        }
        response = await self.request(url=url, params=query_params)
        return response

    async def complete_tasks(
            self,
            ids: List[str],
    ):
        url = TodoServiceConfig.get_task_comlete_url()
        data = {'ids': ids}
        await self.request(url=url, data=data, method=HTTP.POST)


