#!/usr/bin/env python
from functools import partial
import telegram
from time import sleep
from telegram.error import NetworkError, TelegramError
import logging
from auxiliary_file import detect_intent_texts
from environs import Env
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler, Filters, CallbackContext
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def sends_response_user(
    update: Update, context: CallbackContext, project_id
) -> None:
    """Sends the user message."""
    env = Env()
    env.read_env()
    session_id = env.str("TELEGRAM_CHAT_ID")
    bot_log = telegram.Bot(token=env.str('TELEGRAM_LOG'))
    try:
        answer = detect_intent_texts(
            project_id, session_id, update.message.text, 'ru-RU')
        update.message.reply_text(answer.fulfillment_text)

    except NetworkError as network_error:
        bot_log.send_message(
            chat_id=session_id,
            text=f'Ошибка сети tel бота\n{network_error}\n'
        )
        sleep(20)

    except TelegramError as telegram_error:
        bot_log.send_message(
            chat_id=session_id,
            text=f'Ошибка телеграм\n{telegram_error}\n'
        )


def main() -> None:
    while True:

        env = Env()
        env.read_env()
        telegram_token = env.str('TELEGRAM_TOKEN')
        project_id = env.str('PROJECT_ID')

        updater = Updater(telegram_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command, partial(
                sends_response_user, project_id=project_id))
        )
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()
