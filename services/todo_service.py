from datetime import datetime
from typing import List, Dict


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

    @staticmethod
    async def get_tasks(
            user_id: str,
            date: datetime.date,
            repo,
            completed=False,
    ) -> List[Dict]:
        return await repo.get_tasks(
            user_id=user_id,
            date=date,
            completed=completed,
        )

    @staticmethod
    async def complete_tasks(
            ids: List[str],
            repo,
    ) -> None:
        await repo.complete_tasks(ids=ids)


