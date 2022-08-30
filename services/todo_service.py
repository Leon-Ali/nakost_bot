

class TodoService:

    @staticmethod
    async def create_user(user_id: str, repo) -> None:
        await repo.create_user(user_id)



