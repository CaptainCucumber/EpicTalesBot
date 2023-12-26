import logging
import os
from logging.handlers import RotatingFileHandler
import re

import requests
from telegram import Message, Update
from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters

from article_gpt import ArticleGPT
from config import Config
from stt import STT


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler('application.log', maxBytes=1024*1024*20, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


config = Config(os.environ)

# Speech-to-Text
stt = STT(config)
article_gpt = ArticleGPT(config)

async def download_voice(voice_file_id, context):
    # Get the file path from Telegram
    file = context.bot.get_file(voice_file_id)
    file_path = file.file_path

    response = requests.get(file_path)
    return response.content

async def handle_messages(update: Update, context: CallbackContext) -> None:
    message = update.message

    if not is_whitelisted(message):
        await leave_group(context, message)
        return

    if is_bot_mentioned(context.bot.username, message):
        await process_messages(context, message)


async def leave_group(context: CallbackContext, message: Message) -> None:
    await context.bot.leave_chat(message.chat.id)
    logger.warning(
        f"Leaving non-whitelisted group with chat ID {message.chat.id}, "
        f"message type: {message.chat.type} and message: {message.text}"
    )


def is_whitelisted(message: Message) -> bool:
    return message.chat.id in Config.WHITELISTED_GROUPS


def is_bot_mentioned(botname: str, message: Message) -> bool:
    return message.reply_to_message and f'@{botname}' in message.text


async def process_messages(context: CallbackContext, message: Message) -> None:
    replied_message = message.reply_to_message

    if replied_message.voice:
        await handle_voice_message(context, replied_message)
    elif replied_message.text:
        await handle_text_message(context, replied_message)


async def handle_voice_message(context: CallbackContext, message: Message) -> None:
    file = await context.bot.get_file(message.voice.file_id)
    file_url = file.file_path

    transcription = await stt.transcribe_voice(file_url)
    await message.reply_text(transcription)


async def handle_text_message(context: CallbackContext, message: Message) -> None:
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, message.text)

    if urls:
        text = message.text
        summary = article_gpt.summarize(text)
        await message.reply_text(summary)


def main() -> None:
    application = ApplicationBuilder().token(config.get_telegram_token()).build()

    application.add_handler(MessageHandler(filters.ALL, handle_messages))

    application.run_polling()
    
if __name__ == '__main__':
    main()
