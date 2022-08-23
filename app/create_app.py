from aiogram import Bot, Dispatcher

from settings.app import AppConfig


def initialize_app() -> Dispatcher:
    bot = Bot(token=AppConfig.API_TOKEN)
    return Dispatcher(bot)
