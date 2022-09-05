from typing import List

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


multiselect_callback = CallbackData('multiselect', 'item')


class MultiSelect:

    SUBMIT_BTN_NAME = 'завершить'

    async def create(self, items: List):
        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        for item in items:
            inline_kb.insert(types.InlineKeyboardButton(
                item[0],
                callback_data=multiselect_callback.new(item[1])
            ))
        inline_kb.insert(types.InlineKeyboardButton(
            self.SUBMIT_BTN_NAME,
            callback_data=multiselect_callback.new(self.SUBMIT_BTN_NAME)
        ))
        return inline_kb

    async def process_selection(self, query: types.CallbackQuery, data: CallbackData) -> List:
        checked_symbol = '✓'
        items = []

        for item in query['message']['reply_markup']['inline_keyboard']:

            item_key = item[0]['text']
            item_value = item[0]['callback_data'].split(':')[1]

            if item_key == self.SUBMIT_BTN_NAME:
                continue
            elif item_key.startswith(checked_symbol) and data['item'] == item_value:
                items.append((item_key.removeprefix(checked_symbol), item_value))
            elif item_value == data['item']:
                items.append((checked_symbol + ' ' + item_key, item_value))
            else:
                items.append((item_key, item_value))

        if data['item'] == self.SUBMIT_BTN_NAME:
            await query.message.delete_reply_markup()
            return_data = [int(item[1]) for item in items if item[0].startswith(checked_symbol)]
            return return_data

        await query.message.edit_reply_markup(await self.create(items))


@app.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Sends welcome and creates user"""
    user_repo = UsersRepository()
    await TodoService.create_user(user_id=message.from_user.id, repo=user_repo)
    await message.reply(
        "Organizer bot\n\n"
        "Create task: /add\n"
        "Today tasks: /today\n"
        "Tasks by date: /date\n"
        "Test: /test"
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
    tasks_repo = TasksRepository()
    if selected:
        async with state.proxy() as data:
            await TodoService.create_task(
                user_id=callback_query.from_user.id,
                description=data['task_description'],
                date=date.date(),
                repo=tasks_repo,
            )
            await callback_query.message.reply(f'Задача \"{data["task_description"]}\" добавлена')
    await state.finish()


@app.message_handler(commands=['today'])
async def today_tasks(message: types.Message):
    """Sends today tasks"""
    tasks_repo = TasksRepository()
    tasks = await TodoService.get_tasks(
        user_id=message.from_user.id,
        date=message.date.date(),
        repo=tasks_repo,
    )
    tasks_data = [(task['description'], task['id']) for task in tasks]
    await message.reply('Задачи на сегодня', reply_markup=await MultiSelect().create(tasks_data))


@app.message_handler(commands=['date'])
async def tasks_by_date(message: types.Message):
    """Sends tasks by given date"""
    await message.answer()


@app.callback_query_handler(multiselect_callback.filter())
async def complete_tasks(callback_query: types.CallbackQuery, callback_data: CallbackData):
    """Completes tasks"""
    data = await MultiSelect().process_selection(callback_query, callback_data)


if __name__ == '__main__':
    executor.start_polling(app, skip_updates=True)
