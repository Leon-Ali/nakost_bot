from datetime import datetime
from typing import List, Dict

from repositories.users.abstract_repository import AbstractUserRepository
from repositories.tasks.abstract_repository import AbstractTasksRepository


class TodoService:

    @staticmethod
    async def create_user(
            user_id: str,
            repo: AbstractUserRepository,
    ) -> None:
        await repo.create_user(user_id)

    @staticmethod
    async def create_task(
            user_id: str,
            description: str,
            date: datetime.date,
            repo: AbstractTasksRepository,
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
            repo: AbstractTasksRepository,
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
            repo: AbstractTasksRepository,
    ) -> None:
        await repo.complete_tasks(ids=ids)


