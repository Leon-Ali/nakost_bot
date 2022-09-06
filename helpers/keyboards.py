from typing import List

from aiogram import types
from aiogram.utils.callback_data import CallbackData


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
            return_data = [item[1] for item in items if item[0].startswith(checked_symbol)]
            return return_data

        await query.message.edit_reply_markup(await self.create(items))