#!/usr/bin/env python
from functools import partial
import telegram
from time import sleep
from telegram.error import NetworkError, TelegramError
import logging
from answer_dialogflow import detect_intent_texts
from tg_logger_handler import TelegramLogsHandler
from environs import Env
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler, Filters, CallbackContext
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Здравствуйте")


def sends_response_user(
    update: Update, context: CallbackContext,
    project_id, session_id
) -> None:
    """Sends the user message."""
    try:
        answer = detect_intent_texts(
            project_id, session_id, update.message.text, "ru-RU")
        update.message.reply_text(answer.fulfillment_text)

    except NetworkError as network_error:
        logger.error(f"Ошибка сети tel бота\n{network_error}\n")
        sleep(20)

    except TelegramError as telegram_error:
        logger.error(f"Ошибка телеграм\n{telegram_error}\n")


def main() -> None:
    env = Env()
    env.read_env()
    telegram_token = env.str("TELEGRAM_TOKEN")
    project_id = env.str("PROJECT_ID")
    session_id = env.str("TELEGRAM_CHAT_ID")
    bot_log = telegram.Bot(token=env.str("TELEGRAM_LOG"))

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot_log, session_id))

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, partial(
            sends_response_user,
            project_id=project_id,
            session_id=session_id,
        ))
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
