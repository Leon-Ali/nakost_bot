import os


class AppConfig:
    API_TOKEN = os.getenv('API_TOKEN', 'secret')
