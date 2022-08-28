import aiohttp

from settings import TodoServiceConfig


class UsersRepository:

    @staticmethod
    async def create_user(user_id: str):
        headers = {'Authorization': TodoServiceConfig.API_TOKEN, 'Content-Type': 'application/json'}
        url = TodoServiceConfig.get_user_create_url()
        async with aiohttp.ClientSession(headers=headers) as session:
            raw_response = await session.post(url,  json={'user_id': user_id})
            await raw_response.json()
