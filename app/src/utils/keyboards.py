from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..parsers.currency import currency_codes

choice = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Курс валют к рублю 📈")],
        [KeyboardButton(text="Курс валют к доллару🧾")],
        [KeyboardButton(text="Конвертировать валюту 💸")],
        [KeyboardButton(text="О боте 👨‍💻")]
    ],
    resize_keyboard=True,
)

to_main: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Вернуться", callback_data="to main")]]
)

delete = ReplyKeyboardRemove()


async def currency_buttons(page: int) -> InlineKeyboardMarkup:
    """Вызывает функцию которая парсит список кодов валют
    и с помощью KeyboardBuilder создаёт inline кнопки из этих кодов,
    с возможностью переключаться между ними"""
    try:
        currencies = await currency_codes()
        if not currencies:
            return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Возникла ошибка',
                                                                               callback_data='error')]])

        currencies_per_page = 10
        start_index = page * currencies_per_page
        end_index = start_index + currencies_per_page
        currencies_on_page = currencies[start_index:end_index]


        keyboard = InlineKeyboardBuilder()
        for currency in currencies_on_page:
            keyboard.row(InlineKeyboardButton(text=' — '.join(currency), callback_data=f'currency:{currency[0]}'))

        previous_page = page > 0
        next_page = end_index < len(currencies)

        navigation_buttons = []

        if previous_page:
            navigation_buttons.append(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'page:{page - 1}'))

        if next_page:
            navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page:{page + 1}"))

        if navigation_buttons:
            keyboard.row(*navigation_buttons)

        keyboard.row(InlineKeyboardButton(text='На главную', callback_data='to main'))
        return keyboard.as_markup()
    except Exception as e:
        raise e
