from datetime import datetime


class TodoService:

    @staticmethod
    async def create_user(
            user_id: str,
            repo,
    ) -> None:
        await repo.create_user(user_id)

    @staticmethod
    async def create_task(
            user_id: str,
            description: str,
            date: datetime.date,
            repo,
    ) -> None:
        await repo.create_task(
            user_id=user_id,
            description=description,
            date=date,
        )



