import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters
import requests
from google.cloud import speech
from google.oauth2 import service_account
from config import Config, WHITELISTED_GROUPS

TELEGRAM_BOT_TOKEN = Config.get_telegram_token()
GOOGLE_SERVICE_FILE = Config.get_google_service_file()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Google Cloud Speech-to-Text client
credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_FILE) # Update with your credentials path
client = speech.SpeechClient(credentials=credentials)

async def download_voice(voice_file_id, context):
    # Get the file path from Telegram
    file = await context.bot.get_file(voice_file_id)
    file_path = file.file_path

    response = requests.get(file_path)
    return response.content

async def transcribe_voice(voice_data):
    audio = speech.RecognitionAudio(content=voice_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=48000,
        language_code="ru-RU",
        enable_word_confidence=True  # Enable word confidence
    )

    response = client.recognize(config=config, audio=audio)

    # Concatenate all the transcriptions
    transcription = ' '.join([result.alternatives[0].transcript for result in response.results])
    return transcription

async def handle_messages(update: Update, context: CallbackContext) -> None:
    message = update.message

    # Check if the bot is mentioned and if the message is a reply
    if message.reply_to_message and f'@{context.bot.username}' in message.text:

        replied_message = message.reply_to_message

        # Extract the username or first name of the user who sent the replied message
        user = replied_message.from_user
        user_name = user.first_name or user.username  # Prefer first name, fallback to user name

        # Handle voice messages
        if replied_message.voice:
            voice_data = await download_voice(replied_message.voice.file_id, context)
            transcription = await transcribe_voice(voice_data)
            await message.reply_text(f"{user_name} сказал '{transcription}'")

async def validate_access(update: Update, context: CallbackContext) -> None:
    message = update.message

    # If it's a group message and the group is not whitelisted, leave the group
    if message.chat.id not in WHITELISTED_GROUPS:
        await context.bot.leave_chat(message.chat.id)
        logger.warning(f"Leaving non-whitelisted group with chat ID {message.chat.id}, message type: {message.chat.type} and message: {message.text}")
        return

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers are checked in order they are added
    application.add_handler(MessageHandler(filters.ALL, validate_access))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_messages))

    application.run_polling()
    
if __name__ == '__main__':
    main()
