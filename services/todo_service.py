from repositories import UsersRepository


class TodoService:

    async def create_user(self, user_id: str) -> None:
        await UsersRepository.create_user(user_id)



