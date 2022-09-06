from abc import ABC, abstractmethod


class AbstractUserRepository(ABC):

    @abstractmethod
    def create_user(self, user_id: str):
        pass
