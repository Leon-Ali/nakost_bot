from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from aiogram.utils.callback_data import CallbackData

from aiogram_calendar import simple_cal_callback, SimpleCalendar

from create_app import initialize_app
from services import TodoService
from repositories import UsersRepository, TasksRepository


app = initialize_app()


class FSMTask(StatesGroup):
    task_description = State()
    date_choose = State()
    date_confirm = State()


start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_kb.row('Календарь', 'Сегодняшняя дата')


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
    await message.reply('Выберите дату для задачи', reply_markup=start_kb)


@app.message_handler(Text(equals=['Сегодняшняя дата'], ignore_case=True), state=FSMTask.date_choose)
async def create_today_task(message: types.Message, state: FSMContext):
    tasks_repo = TasksRepository()
    async with state.proxy() as data:
        await TodoService.create_task(
            user_id=message.from_user.id,
            description=data['task_description'],
            date=message.date.date(),
            repo=tasks_repo,
        )
    await message.reply(f'Задача \"{data["task_description"]}\" добавлена')
    await state.finish()


@app.message_handler(Text(equals=['Календарь'], ignore_case=True), state=FSMTask.date_choose)
async def choose_task_date(message: types.Message):
    """Adds task date"""
    await FSMTask.next()
    await message.reply("Выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())


@app.callback_query_handler(simple_cal_callback.filter(), state=FSMTask.date_confirm)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    print(callback_data)
    if selected:
        await callback_query.message.reply(
            f'You selected {date.strftime("%d/%m/%Y")}',
        )
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
