import logging
import os
import re

import requests
from article_gpt import ArticleGPT
from config import Config

from log_config import setup_logging
from stt import STT
from telegram import Message, Update
from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters
from video_gpt import VideoGPT


setup_logging()
logger = logging.getLogger(__name__)

config = Config(os.environ)

# Speech-to-Text
stt = STT(config)
article_gpt = ArticleGPT(config)
video_gpt = VideoGPT(config)

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


def is_youtube_url(url: str) -> bool:
    return 'youtube.com/watch' in url or 'youtu.be/' in url


async def process_messages(context: CallbackContext, message: Message) -> None:
    replied_message = message.reply_to_message

    if replied_message.voice:
        await handle_voice_message(context, replied_message)
    elif replied_message.text:
        await handle_text_message(context, replied_message)


def escape_markdown(text):
    escape_chars = '[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])


async def handle_voice_message(context: CallbackContext, message: Message) -> None:
    logger.info(f'New voice message from chat ID {message.chat.id} and user ID {message.from_user.id}({message.from_user.name})')

    file = await context.bot.get_file(message.voice.file_id)
    file_url = file.file_path

    transcription = await stt.transcribe_voice(file_url)
    escaped_text = escape_markdown(f"_{transcription}_")
    await message.reply_text(escaped_text, parse_mode='MarkdownV2')


async def handle_text_message(context: CallbackContext, message: Message) -> None:
    logger.info(f'New text message from chat ID {message.chat.id} and user ID {message.from_user.id}({message.from_user.name})')
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, message.text)

    if not urls:
        logger.warning(f'No URL found in message: {message.text}')
        return
    
    summary = None
    if is_youtube_url(urls[0]):
        summary = video_gpt.summarize(urls[0])
       
    else:
        summary = article_gpt.summarize(urls[0])

    escaped_text = escape_markdown(summary)
    await message.reply_text(escaped_text, parse_mode='MarkdownV2')


def main() -> None:
    application = ApplicationBuilder().token(config.get_telegram_token()).build()

    application.add_handler(MessageHandler(filters.ALL, handle_messages))

    application.run_polling()
    
if __name__ == '__main__':
    main()
