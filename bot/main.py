import logging
import os
from logging.handlers import RotatingFileHandler
import re

import requests
from telegram import Update
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

    # If it's a group message and the group is not whitelisted, leave the group
    if message.chat.id not in Config.WHITELISTED_GROUPS:
        await context.bot.leave_chat(message.chat.id)
        logger.warning(f"Leaving non-whitelisted group with chat ID {message.chat.id}, message type: {message.chat.type} and message: {message.text}")
        return

    # Check if the bot is mentioned and if the message is a reply
    if message.reply_to_message and f'@{context.bot.username}' in message.text:

        replied_message = message.reply_to_message

        # Extract the username or first name of the user who sent the replied message
        user = replied_message.from_user
        user_name = user.first_name or user.username  # Prefer first name, fallback to user name

        # Handle voice messages
        if replied_message.voice:
            file = await context.bot.get_file(replied_message.voice.file_id)
            file_url = file.file_path

            transcription = await stt.transcribe_voice(file_url)
            await message.reply_text(f"{user_name} сказал '{transcription}'")
        elif replied_message.text:
            url_pattern = r'https?://[^\s]+'
            url = re.findall(url_pattern, replied_message.text)
            if url:
                text = replied_message.text
                summary = article_gpt.summarize(text)
                await message.reply_to_message.reply_text(summary)


def main() -> None:
    application = ApplicationBuilder().token(config.get_telegram_token()).build()

    application.add_handler(MessageHandler(filters.ALL, handle_messages))

    application.run_polling()
    
if __name__ == '__main__':
    main()
