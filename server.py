from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from aiogram.utils.callback_data import CallbackData

from aiogram_calendar import simple_cal_callback, SimpleCalendar

from create_app import initialize_app
from services import TodoService
from repositories import UsersRepository, TasksRepository
from helpers.keyboards import MultiSelect, multiselect_callback

app, bot = initialize_app()


class FSMTask(StatesGroup):
    """Task creation state"""
    task_description = State()
    date_choose = State()
    date_confirm = State()


start_kb = types.InlineKeyboardMarkup(row_width=2)

text_and_data = (
    ('Календарь', 'календарь'),
    ('Сегодняшняя дата', 'сегодняшняя дата'),
)

row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

start_kb.row(*row_btns)


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
    await bot.send_message(chat_id=message.chat.id, text='Введите описание задачи')


@app.message_handler(state=FSMTask.task_description)
async def add_task_description(message: types.Message, state: FSMContext):
    """Adds task description"""
    async with state.proxy() as data:
        data['task_description'] = message.text
    await FSMTask.next()
    await bot.send_message(chat_id=message.chat.id, text='Выберите дату для задачи', reply_markup=start_kb)


@app.callback_query_handler(Text(equals=['Сегодняшняя дата'], ignore_case=True), state=FSMTask.date_choose)
async def create_today_task(query: types.CallbackQuery, state: FSMContext):
    """Create task for current date"""
    tasks_repo = TasksRepository()

    async with state.proxy() as data:
        await TodoService.create_task(
            user_id=query['from'].id,
            description=data['task_description'],
            date=query.message.date.date(),
            repo=tasks_repo,
        )
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f'Задача \"{data["task_description"]}\" добавлена',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


@app.callback_query_handler(Text(equals=['Календарь'], ignore_case=True), state=FSMTask.date_choose)
async def choose_task_date(query: types.CallbackQuery):
    """Add task date"""
    await FSMTask.next()
    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Выберите дату: ",
        reply_markup=await SimpleCalendar().start_calendar(),
    )


@app.callback_query_handler(simple_cal_callback.filter(), state=FSMTask.date_confirm)
async def process_task_add_calendar_date(
        callback_query: types.CallbackQuery,
        callback_data: CallbackData,
        state: FSMContext,
):
    """Create task with date from calendar"""
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    tasks_repo = TasksRepository()
    if selected:
        async with state.proxy() as data:
            await TodoService.create_task(
                user_id=callback_query.from_user.id,
                description=data['task_description'],
                date=date.date(),
                repo=tasks_repo,
            )
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text=f'Задача \"{data["task_description"]}\" добавлена',
                reply_markup=types.ReplyKeyboardRemove(),
            )
    await state.finish()


@app.message_handler(commands=['today'])
async def get_today_tasks(message: types.Message):
    """Sends today tasks"""
    tasks_repo = TasksRepository()
    tasks = await TodoService.get_tasks(
        user_id=message.from_user.id,
        date=message.date.date(),
        repo=tasks_repo,
    )
    if tasks:
        tasks_data = [(task['description'], task['id']) for task in tasks]
        await message.reply('Задачи на сегодня', reply_markup=await MultiSelect().create(tasks_data))
    else:
        await message.reply('Задач на сегодня нет')


@app.message_handler(commands=['date'])
async def get_tasks_by_date(message: types.Message):
    """Show calendar for choosing date"""
    await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите дату ",
        reply_markup=await SimpleCalendar().start_calendar(),
    )


@app.callback_query_handler(simple_cal_callback.filter())
async def process_tasks_get_calendar_date(callback_query: types.CallbackQuery, callback_data: CallbackData):
    """Get tasks for date from calendar"""
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    tasks_repo = TasksRepository()
    if selected:
        tasks = await TodoService.get_tasks(
            user_id=callback_query.from_user.id,
            date=date.date(),
            repo=tasks_repo,
        )
        if tasks:
            tasks_data = [(task['description'], task['id']) for task in tasks]
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text='Задачи на сегодня',
                reply_markup=await MultiSelect().create(tasks_data),
            )
        else:
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text=f'Задач на дату {str(date.date())} нет',
            )


@app.callback_query_handler(multiselect_callback.filter())
async def complete_tasks(callback_query: types.CallbackQuery, callback_data: CallbackData):
    """Completes tasks"""
    data = await MultiSelect().process_selection(callback_query, callback_data)
    if data:
        tasks_repo = TasksRepository()
        await TodoService.complete_tasks(
            ids=data,
            repo=tasks_repo,
        )
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text='Выбранные задачи завершены',
        )


if __name__ == '__main__':
    executor.start_polling(app, skip_updates=True)
