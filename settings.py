import os

from dotenv import load_dotenv


BASE_PATH = os.path.dirname(__file__) + '/'

load_dotenv(str(BASE_PATH + '.env'))


class AppConfig:
    API_TOKEN = os.getenv('API_TOKEN', 'secret')


class TodoServiceConfig:
    API_TOKEN = os.getenv('TODO_SERVICE_TOKEN', 'secret')
    BASE_URL = os.getenv('TODO_SERVICE_BASE_URL', 'http://example.com')
    USERS_URL = os.getenv('TODO_SERVICE_USER_URL', 'users')
    TASKS_URL = os.getenv('TODO_SERVICE_TASKS_URL', 'tasks')
    TASKS_COMPLETE_URL = os.getenv('TODO_SERVICE_TASKS_COMPLETE_URL', 'complete')

    @classmethod
    def get_user_create_url(cls):
        return f'{cls.BASE_URL}/{cls.USERS_URL}/'

    @classmethod
    def get_task_create_url(cls):
        return f'{cls.BASE_URL}/{cls.TASKS_URL}/'

    @classmethod
    def get_task_comlete_url(cls):
        return f'{cls.BASE_URL}/{cls.TASKS_URL}/{cls.TASKS_COMPLETE_URL}/'
