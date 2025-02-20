import os
import decimal

import aiohttp
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL2')

async def currency_codes() -> list:
    """Выводит список буквенных кодов и их курсы (при необходимости)"""
    currency_dict = {
        "AED": "Объединенные Арабские Эмираты",
        "AFN": "Афганистан",
        "ALL": "Албания",
        "AMD": "Армения",
        "ANG": "Нидерландские Антильские острова",
        "AOA": "Ангола",
        "ARS": "Аргентина",
        "AUD": "Австралия",
        "AWG": "Аруба",
        "AZN": "Азербайджан",
        "BAM": "Босния и Герцеговина",
        "BBD": "Барбадос",
        "BDT": "Бангладеш",
        "BGN": "Болгария",
        "BHD": "Бахрейн",
        "BIF": "Бурунди",
        "BMD": "Бермуды",
        "BND": "Бруней",
        "BOB": "Боливия",
        "BRL": "Бразилия",
        "BSD": "Багамы",
        "BTN": "Бутан",
        "BWP": "Ботсвана",
        "BYN": "Беларусь",
        "BZD": "Белиз",
        "CAD": "Канада",
        "CDF": "Демократическая Республика Конго",
        "CHF": "Швейцария",
        "CLP": "Чили",
        "CNY": "Китай",
        "COP": "Колумбия",
        "CRC": "Коста-Рика",
        "CUP": "Куба",
        "CVE": "Кабо-Верде",
        "CZK": "Чехия",
        "DJF": "Джибути",
        "DKK": "Дания",
        "DOP": "Доминиканская Республика",
        "DZD": "Алжир",
        "EGP": "Египет",
        "ERN": "Эритрея",
        "ETB": "Эфиопия",
        "EUR": "Европейский союз",
        "FJD": "Фиджи",
        "FKP": "Фолклендские острова",
        "FOK": "Фарерские острова",
        "GBP": "Великобритания",
        "GEL": "Грузия",
        "GGP": "Гернси",
        "GHS": "Гана",
        "GIP": "Гибралтар",
        "GMD": "Гамбия",
        "GNF": "Гвинея",
        "GTQ": "Гватемала",
        "GYD": "Гайана",
        "HKD": "Гонконг",
        "HNL": "Гондурас",
        "HRK": "Хорватия",
        "HTG": "Гаити",
        "HUF": "Венгрия",
        "IDR": "Индонезия",
        "ILS": "Израиль",
        "IMP": "Остров Мэн",
        "INR": "Индия",
        "IQD": "Ирак",
        "IRR": "Иран",
        "ISK": "Исландия",
        "JEP": "Джерси",
        "JMD": "Ямайка",
        "JOD": "Иордания",
        "JPY": "Япония",
        "KES": "Кения",
        "KGS": "Кыргызстан",
        "KHR": "Камбоджа",
        "KID": "Кирибати",
        "KMF": "Коморы",
        "KRW": "Южная Корея",
        "KWD": "Кувейт",
        "KYD": "Каймановы острова",
        "KZT": "Казахстан",
        "LAK": "Лаос",
        "LBP": "Ливан",
        "LKR": "Шри-Ланка",
        "LRD": "Либерия",
        "LSL": "Лесото",
        "LYD": "Ливия",
        "MAD": "Марокко",
        "MDL": "Молдова",
        "MGA": "Мадагаскар",
        "MKD": "Северная Македония",
        "MMK": "Мьянма",
        "MNT": "Монголия",
        "MOP": "Макао",
        "MRU": "Мавритания",
        "MUR": "Маврикий",
        "MVR": "Мальдивы",
        "MWK": "Малави",
        "MXN": "Мексика",
        "MYR": "Малайзия",
        "MZN": "Мозамбик",
        "NAD": "Намибия",
        "NGN": "Нигерия",
        "NIO": "Никарагуа",
        "NOK": "Норвегия",
        "NPR": "Непал",
        "NZD": "Новая Зеландия",
        "OMR": "Оман",
        "PAB": "Панама",
        "PEN": "Перу",
        "PGK": "Папуа — Новая Гвинея",
        "PHP": "Филиппины",
        "PKR": "Пакистан",
        "PLN": "Польша",
        "PYG": "Парагвай",
        "QAR": "Катар",
        "RON": "Румыния",
        "RSD": "Сербия",
        "RUB": "Россия",
        "RWF": "Руанда",
        "SAR": "Саудовская Аравия",
        "SBD": "Соломоновы Острова",
        "SCR": "Сейшельские Острова",
        "SDG": "Судан",
        "SEK": "Швеция",
        "SGD": "Сингапур",
        "SHP": "Остров Святой Елены",
        "SLE": "Сьерра-Леоне",
        "SOS": "Сомали",
        "SRD": "Суринам",
        "SSP": "Южный Судан",
        "STN": "Сан-Томе и Принсипи",
        "SYP": "Сирия",
        "SZL": "Эсватини",
        "THB": "Таиланд",
        "TJS": "Таджикистан",
        "TMT": "Туркменистан",
        "TND": "Тунис",
        "TOP": "Тонга",
        "TRY": "Турция",
        "TTD": "Тринидад и Тобаго",
        "TVD": "Тувалу",
        "TWD": "Тайвань",
        "TZS": "Танзания",
        "UAH": "Украина",
        "UGX": "Уганда",
        "USD": "Соединенные Штаты",
        "UYU": "Уругвай",
        "UZS": "Узбекистан",
        "VES": "Венесуэла",
        "VND": "Вьетнам",
        "VUV": "Вануату",
        "WST": "Самоа",
        "XAF": "КФА (Центральная Африка)",
        "XCD": "Восточно-Карибский доллар",
        "XDR": "Специальные права заимствования",
        "XOF": "КФА (Западная Африка)",
        "XPF": "Французская Полинезия",
        "YER": "Йемен",
        "ZAR": "Южная Африка",
        "ZMW": "Замбия",
        "ZWL": "Зимбабве"
    }
    return [[k, v] for k, v in currency_dict.items()]


async def currency_rates() -> list:
    """Парсит курсы обмена и возвращает список"""
    url = URL + 'USD'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        if data["result"] == "success":
            exchange_rates = data["rates"]
            return format_courses_for_telegram(exchange_rates)
    except aiohttp.ClientError as e:
        raise e

    except KeyError as e:
        raise e

    except Exception as e:
        raise e


async def get_exchange_rates(from_currency: str, to_currency: str) -> float:
    """Получает курс обмена между двумя валютами с использованием API без каких либо формул"""
    url = URL + from_currency
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        if data["result"] == "success":
            exchange_rates = data["rates"]
            if to_currency in exchange_rates:
                return exchange_rates[to_currency]
            else:
                raise
        else:
            raise

    except aiohttp.ClientError as e:
        raise e

    except KeyError as e:
        raise e

    except Exception as e:
        raise e


async def convert_currency(from_currency: str, to_currency: str, amount: str):
    """Парсит курс обмена одной валюты к другой
    и с помощью формулы выводит конвертированную сумму"""
    try:
        if amount in ",":
            amount = amount.replace(",", ".")

        try:
            amount = decimal.Decimal(amount)
            if amount <= 0:
                return "Сумма должна быть больше нуля"
        except decimal.InvalidOperation:
            return "Некорректный формат суммы. Используйте только цифры и точку/запятую как разделитель."

        exchange_rate = await get_exchange_rates(from_currency, to_currency)
        if isinstance(exchange_rate, float):
            converted_amount = amount * decimal.Decimal(str(exchange_rate))
            return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
        else:
            return exchange_rate
    except Exception as e:
        raise e



def format_courses_for_telegram(courses: dict) -> str:
    """Форматирует словарь для удобного чтения пользователем"""
    if not courses:
        return "Нет данных о курсах валют."

    formatted_lines = []
    for code, details in courses.items():
        formatted_lines.append(
            f"{code}: {details}"
        )
    return "\n".join(sorted(formatted_lines))