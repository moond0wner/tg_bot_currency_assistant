import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    """Считывает каждое взаимодействие пользователей с ботом и обрабатывает ошибки"""
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        logger.info(f'User "{event.from_user.username}" ({event.from_user.id}) '
                    f'отправил: {event.text if isinstance(event, Message) else event.data}')

        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(f"Возникла ошибка при обработке {event.from_user.id}: {e}")
            raise e