from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_app import initialize_app
from services import TodoService
from repositories import UsersRepository


app = initialize_app()


class FSMTask(StatesGroup):
    task_description = State()
    date = State()


@app.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Sends welcome and creates user"""
    user_repo = UsersRepository()
    await TodoService.create_user(user_id=message.from_user.id, repo=user_repo)
    await message.reply(
        "Organizer bot\n\n"
        "Create task: /add\n"
        "Today tasks: /today\n"
        "Tasks by date: /date"
    )


@app.message_handler(commands=['add'])
async def add_task(message: types.Message):
    """Adds new task"""
    await FSMTask.task_description.set()
    await message.reply('Введите имя задачи')


@app.message_handler(state=FSMTask.task_description)
async def add_task_description(message: types.Message, state: FSMContext):
    """Adds task description"""
    async with state.proxy() as data:
        data['task_description'] = message.text
    await FSMTask.next()
    await message.reply('Выберите дату для задачи')


@app.message_handler(state=FSMTask.date)
async def add_task_date(message: types.Message, state: FSMContext):
    """Adds task date"""
    async with state.proxy() as data:
        data['date'] = message.date

    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()


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
