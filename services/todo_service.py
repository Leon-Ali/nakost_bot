from repositories import UsersRepository
from settings import TodoServiceConfig


class TodoService:

    def __init__(self):
        self.headers = {'X-API-KEY': TodoServiceConfig.API_TOKEN, 'Content-Type': 'application/json'}

    async def create_user(self, user_id: str) -> None:
        await UsersRepository.create_user(user_id, self.headers)



