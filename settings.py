import os

from dotenv import load_dotenv


BASE_PATH = os.path.dirname(__file__) + '/'

load_dotenv(str(BASE_PATH + '.env'))


class AppConfig:
    API_TOKEN = os.getenv('API_TOKEN', 'secret')
