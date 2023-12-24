import logging
import os
from logging.handlers import RotatingFileHandler

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters

from bot.config import Config
from bot.stt import STT

TELEGRAM_BOT_TOKEN = Config.get_telegram_token()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler('application.log', maxBytes=1024*1024*20, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


config = Config(os.environ)

# Speech-to-Text
stt = STT(config)

async def download_voice(voice_file_id, context):
    # Get the file path from Telegram
    file = await context.bot.get_file(voice_file_id)
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
            voice_data = await download_voice(replied_message.voice.file_id, context)
            transcription = await stt.transcribe_voice(voice_data)
            await message.reply_text(f"{user_name} сказал '{transcription}'")


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL, handle_messages))

    application.run_polling()
    
if __name__ == '__main__':
    main()
