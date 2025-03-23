import os
import asyncio
from dotenv import load_dotenv
from .logging import logger
from .exception_handlers import exception_handler
from ..utils.retry_connection import retry_connection
from telegram import Bot as TelegramBot

load_dotenv()


@exception_handler(default_return=False)
@retry_connection()
def init_telegram_bot() -> TelegramBot:
    """
    Initializes and returns a Telegram bot instance.

    Returns:
        TelegramBot: An instance of the Telegram bot.
    """
    TELEGRAM_API_SECRET = os.environ["TELEGRAM_API_SECRET"]
    return TelegramBot(token=TELEGRAM_API_SECRET)


@exception_handler(default_return=False)
@retry_connection()
def send_telegram(chat_id: str, msg: str) -> bool:
    """
    Sends a message to a specific Telegram chat.

    Args:
        chat_id (str): The Telegram chat ID where the message should be sent.
        msg (str): The message content.

    Returns:
        bool: True if the message was sent successfully.
    """
    telegram_bot = init_telegram_bot()

    if telegram_bot:
        asyncio.run(telegram_bot.send_message(chat_id=chat_id, text=msg))
        logger.info(f"Telegram {chat_id}: {msg}, sent succesfully.")
        return True

    return False
