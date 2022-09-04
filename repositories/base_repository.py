from settings import TodoServiceConfig


class BaseRepository:
    headers = {'X-API-KEY': TodoServiceConfig.API_TOKEN, 'Content-Type': 'application/json'}