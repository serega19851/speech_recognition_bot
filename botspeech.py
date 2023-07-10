#!/usr/bin/env python

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


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    session_id = env.str("TELEGRAM_CHAT_ID")
    answer = detect_intent_texts(
        project_id, session_id, update.message.text, 'ru-RU')
    update.message.reply_text(answer.fulfillment_text)


def main() -> None:
    env = Env()
    env.read_env()
    telegram_token = env.str('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
