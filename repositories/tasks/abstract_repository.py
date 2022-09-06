from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict


class AbstractTasksRepository(ABC):

    @abstractmethod
    async def create_task(
            self,
            user_id: str,
            description: str,
            date: datetime.date,
    ) -> None:
        pass

    @abstractmethod
    async def get_tasks(
            self,
            user_id: str,
            date: datetime.date,
            completed=False,
    ) -> List[Dict]:
        pass

    @abstractmethod
    async def complete_tasks(
            self,
            ids: List[str],
    ) -> None:
        pass
