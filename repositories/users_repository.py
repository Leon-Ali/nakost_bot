import aiohttp
from settings import TodoServiceConfig


class UsersRepository:

    def __init__(self):
        self.headers = {'X-API-KEY': TodoServiceConfig.API_TOKEN, 'Content-Type': 'application/json'}

    async def create_user(self, user_id: str):
        url = TodoServiceConfig.get_user_create_url()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            raw_response = await session.post(url,  json={'user_id': user_id})
            await raw_response.json()
