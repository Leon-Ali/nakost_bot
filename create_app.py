from typing import Tuple

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import AppConfig


def initialize_app() -> Tuple[Dispatcher, Bot]:
    storage = MemoryStorage()
    bot = Bot(token=AppConfig.API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    return dp, bot
