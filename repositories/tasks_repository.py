from datetime import datetime

import aiohttp
from settings import TodoServiceConfig

from .base_repository import BaseRepository


class TasksRepository(BaseRepository):

    async def create_task(
            self,
            user_id: str,
            description: str,
            date: datetime.date,
    ):
        url = TodoServiceConfig.get_task_create_url()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            data = {
                'user': user_id,
                'description': description,
                'date': str(date),
            }
            raw_response = await session.post(url, json=data)
            await raw_response.json()
