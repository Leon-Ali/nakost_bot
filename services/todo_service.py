from repositories import UsersRepository


class TodoService:

    @staticmethod
    async def create_user(user_id: str) -> None:
        await UsersRepository.create_user(user_id)



