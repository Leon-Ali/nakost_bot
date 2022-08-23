from aiogram import Bot, Dispatcher

from settings import AppConfig


def initialize_app() -> Dispatcher:
    bot = Bot(token=AppConfig.API_TOKEN)
    return Dispatcher(bot)
