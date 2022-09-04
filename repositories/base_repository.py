import aiohttp
from aiohttp.web_response import json_response

from settings import TodoServiceConfig


class BaseRepository:
    headers = {'X-API-KEY': TodoServiceConfig.API_TOKEN, 'Content-Type': 'application/json'}

    async def request(self, url, params=None, data=None, method='get') -> json_response():
        async with aiohttp.ClientSession(headers=self.headers) as session:
            request_method = getattr(session, method)
            raw_response = await request_method(url, json=data, params=params)
            return await raw_response.json()
