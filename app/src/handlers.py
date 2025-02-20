import os
import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from dotenv import load_dotenv

from .parsers.cb_course import parse_course, format_courses_for_telegram
from .parsers.currency import currency_codes, convert_currency, currency_rates
from .utils import keyboards as kb

router = Router()
load_dotenv()
URL = os.getenv("URL1")


class Currency(StatesGroup):
    """Класс состояний для хранения валют и суммы конвертации"""
    from_currency = State()
    to_currency = State()
    amount = State()



@router.message(CommandStart())
async def start(message: Message):
    """Стартовый обработчик"""
    await message.answer(
        f"Здравствуйте <b>{message.from_user.full_name}</b> 👋, выберите что Ваc интересует.",
            reply_markup=kb.choice,  parse_mode='HTML'
    )


@router.message(F.text.lower() == "курс валют к рублю 📈")
async def show_ruble_rates(message: Message):
    """Вызывает функцию которая парсит валюты относительно рубля, форматирует текст и отправляет"""
    try:
        await message.answer("Получаю курсы валют, ожидайте...⏳", reply_markup=kb.delete)
        courses = await parse_course(URL)
        await asyncio.sleep(1.5)
        if courses:
            formatted_courses = format_courses_for_telegram(courses)
            await message.answer(
                "<b>Курсы иностранных валют к рублю Российской Федерации на сегодня:</b>", parse_mode='HTML'
            )
            await message.answer(f'<b>{formatted_courses}</b>', reply_markup=kb.to_main, parse_mode='HTML')
        else:
            await message.answer("<i>Не удалось получить курсы валют 😕</i>", reply_markup=kb.to_main, parse_mode='HTML')
    except Exception:
        await message.answer("<i>Не удалось получить курсы валют 😕</i>", reply_markup=kb.to_main, parse_mode='HTML')
        raise



@router.message(F.text.lower() == 'курс валют 🧾')
async def show_exchange_rates(message: Message):
    """Вызывает функцию которая парсит валюты, форматирует текст и отправляет"""
    try:
        await message.answer("Получаю курсы валют, ожидайте...⏳", reply_markup=kb.delete)
        courses = await currency_rates()
        await asyncio.sleep(1.5)
        if courses:
            await message.answer("<b>Курсы валют относительно USD: </b>", parse_mode='HTML')
            await message.answer(f'<b>{courses}</b>', parse_mode='HTML')

            await asyncio.sleep(1.5)
            await message.answer("<i>Коды валют используются по <b>ISO 4217</b>, ознакомиться с ними можно "
                                 "по <a href='https://www.exchangerate-api.com/docs/supported-currencies'>ссылке."
                                 "</a></i>",
                                 reply_markup=kb.to_main)
        else:
            await message.answer("<i>Не удалось получить курсы валют 😕</i>", reply_markup=kb.to_main, parse_mode='HTML')
    except Exception:
        await message.answer("<i>Не удалось получить курсы валют 😕</i>", reply_markup=kb.to_main, parse_mode='HTML')
        raise



@router.message(F.text.lower() == "конвертировать валюту 💸")
async def get_from_currency(message: Message, state: FSMContext):
    """Обрабатывает информацию о валюте"""
    await message.answer("<i>Подождите, собираю список валют...</i>", reply_markup=kb.delete, parse_mode='HTML')
    await asyncio.sleep(2)
    await message.answer(
        "<ins><i>Выберите валюту из которой хотите конвертировать:</i></ins>", reply_markup=await kb.currency_buttons(0),
                                                                        parse_mode='HTML'
    )
    await state.set_state(Currency.from_currency)



@router.callback_query(Currency.from_currency, F.data.startswith('currency:'))
async def get_to_currency(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает информацию о валюте"""
    currency = callback.data.split(':')[1]
    await state.update_data(from_currency=currency)
    await callback.answer(f"Вы выбрали валюту: {currency}")

    new_text = 'Выберите валюту в которую хотите конвертировать:'
    try:
        if callback.message.text != new_text:
            await callback.message.edit_text(f'<ins><i>{new_text}</i></ins>',
                                             reply_markup=await kb.currency_buttons(0), parse_mode='HTML')
            await state.set_state(Currency.to_currency)
    except TelegramBadRequest as e:
        raise e



@router.callback_query(Currency.to_currency, F.data.startswith('currency:'))
async def get_amount(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает сумму для конвертации"""
    currency = callback.data.split(':')[1]
    await state.update_data(to_currency=currency)
    await callback.answer(f"Вы выбрали валюту: {currency}")
    await callback.message.edit_text("<ins><i>Теперь введите сумму для конвертации</i></ins>", parse_mode='HTML')
    await state.set_state(Currency.amount)



@router.message(Currency.amount)
async def print_convert(message: Message, state: FSMContext):
    """Вызывает функцию, которая конвертирует сумму и выводит результат"""
    await state.update_data(amount=str(message.text))
    data = await state.get_data()
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    amount = data.get("amount")
    if not from_currency or not to_currency:
        await message.answer("Пожалуйста, выберите валюты заново❗")
        await state.clear()
        return

    converted_result = await convert_currency(from_currency, to_currency, amount)
    await message.answer(converted_result, reply_markup=kb.to_main)
    await state.clear()



@router.callback_query(F.data.startswith('page:'))
async def pagination(callback: CallbackQuery):
    """Переключает страницы inline кнопок при выборе валют"""
    page = int(callback.data.split(':')[1])
    keyboard = await kb.currency_buttons(page)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()



@router.message(F.text.lower() == 'о боте 👨‍💻')
async def information_about_bot(message: Message):
    """Выводит информацию о боте"""
    await message.answer(
    '<b><i>Привет 🖐\n' 
        'Этот бот был создан для развития моих навыков в сфере бото-строения, а также с целью помочь быстро '
         'получать актуальную информацию о курсах валют и её конвертации.\n'
        'Хочу предупредить, что тариф хостинга на котором находится бот самый дешевый '
        'и поэтому бот может быть в некоторых моментах долго обрабатывать запрос.\n'
        'Курсы валют и конвертация их предоставлена <a href="https://www.exchangerate-api.com">Exchangerate-api.com</a>.\n'
        'Больше моих работ Вы можете увидеть в моём <b><u><a href="https://github.com/moond0wner">Github</a></u></b> 🧐.\n'
        'Если Вы нашли ошибку/недочёт, хотите оставить отзыв о моём боте или желаете заказать разработку бота: '
        '<b><u><a href="https://t.me/nevertoolate00">Telegram</a></u></b>.'
        '</i></b>',
        reply_markup=kb.to_main, parse_mode='HTML')



@router.callback_query(F.data == 'to main')
async def to_main(callback: CallbackQuery):
    """Возвращает в выбор услуг"""
    await callback.answer()
    await callback.message.answer("<i>Перемещаю Вас в главное меню...⌚</i>", parse_mode='HTML')
    await asyncio.sleep(2.5)
    await callback.message.answer('<b>Выберите что Вас интересует.</b>', reply_markup=kb.choice, parse_mode='HTML')


@router.callback_query(F.data == 'error')
async def check_to_error(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("<i>Возникла ошибка, обратитесь к разработчику</i>", reply_markup=kb.to_main, parse_mode='HTML')