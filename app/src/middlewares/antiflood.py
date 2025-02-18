from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """Уменьшает частоту обработки сообщений при спаме
    Если пользователь флудит /start или inline кнопками,
    то в течение 2 секунд запросы не обрабатываются"""
    def __init__(self, time_limit: int=2) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)


    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str,  Any]
    ) -> Any:
        if event.from_user.id in self.limit:
            await event.answer("Пожалуйста, не флудите...", show_alert=True)
            return
        else:
            self.limit[event.from_user.id] = None
        return await handler(event, data)

