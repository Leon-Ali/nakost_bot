from aiogram import executor, types

from create_app import initialize_app


app = initialize_app()


@app.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply(
        "Бот ораганайзер\n\n"
        "Добавить задачу: /add\n"
        "Сегодняшние задачи: /today\n"
        "По дате: /date"
    )


@app.message_handler(commands=['add'])
async def add_task(message: types.Message):
    """Добавляет новую задачу"""
    # 1 введите задачу
    # 2 введите дату или выберите сегодняшнюю дату
    await message.reply()


@app.message_handler(commands=['today'])
async def today_tasks(message: types.Message):
    """Отправляет задачи на сегодня"""
    await message.answer()


@app.message_handler(commands=['date'])
async def tasks_by_date(message: types.Message):
    """Отправляет задачи на конкретную дату"""
    await message.answer()


@app.message_handler(commands=['complete'])
async def complete_tasks(message: types.Message):
    """Завершает таски"""
    await message.answer()


if __name__ == '__main__':
    executor.start_polling(app, skip_updates=True)
