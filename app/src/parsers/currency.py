import os
import decimal

import aiohttp
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL2')

async def list_currency_codes(show_exchange: bool = True) -> str:
    """Выводит список буквенных кодов и их курсы (при необходимости)"""
    url = URL + 'USD' # так как просто нужен список кодов, то смысла нет с какой валютой парсить
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        if data['result'] == 'success':
            dict_currency = data['rates']
            if show_exchange:
                formatted_lines = []
                for code, exchange in dict_currency.items():
                    formatted_lines.append(
                        f"{code}: {exchange}"
                    )
                return "\n".join(sorted(formatted_lines))
            else:
                return sorted(dict_currency)

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
