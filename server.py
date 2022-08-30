from aiogram import executor, types

from create_app import initialize_app
from services import TodoService
from repositories import UsersRepository


app = initialize_app()


@app.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Sends welcome and creates user"""
    await TodoService.create_user(user_id=message.from_user.id, repo=UsersRepository)
    await message.reply(
        "Organizer bot\n\n"
        "Create task: /add\n"
        "Today tasks: /today\n"
        "Tasks by date: /date"
    )


@app.message_handler(commands=['add'])
async def add_task(message: types.Message):
    """Adds new task"""
    # 1 введите задачу
    # 2 введите дату или выберите сегодняшнюю дату
    await message.reply()


@app.message_handler(commands=['today'])
async def today_tasks(message: types.Message):
    """Sends today tasks"""
    await message.answer()


@app.message_handler(commands=['date'])
async def tasks_by_date(message: types.Message):
    """Sends tasks by given date"""
    await message.answer()


@app.message_handler(commands=['complete'])
async def complete_tasks(message: types.Message):
    """Completes tasks"""
    await message.answer()


if __name__ == '__main__':
    executor.start_polling(app, skip_updates=True)
