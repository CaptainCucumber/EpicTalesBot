import logging
import re

from article_gpt import ArticleGPT
from config import Config, config
from localization import _
from metrics import track_function
from stt import STT
from telegram import Message, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from video_gpt import VideoGPT

logger = logging.getLogger(__name__)

# Speech-to-Text
stt = STT(config)
article_gpt = ArticleGPT(config)
video_gpt = VideoGPT(config)


READING_STICKER = "CAACAgEAAxkBAAPvZa08i8gvG70My_EEkqmhgwvLu5gAAqECAAKoyCFEr-C6Suk25ik0BA"
WATCHING_STICKER = "CAACAgEAAxkBAAPzZa09iinK8z-W-mNnUp0YPHLDpkwAAhsCAAPUGESSRmhdQDpGTTQE"
LISTENING_STICKER = "CAACAgEAAxkBAAP7Za1GmGxnW7OUXAy5-e6tIqgGZVwAAtcCAAKkdyBEDjNwiD91jjI0BA"

@track_function
async def handle_messages(update: Update, context: CallbackContext) -> None:
    message = update.message if update.message else update.channel_post

    if not message:
        logger.warning("Received message with no content")
        return

    if is_blacklisted(message):
        leave_group(context, message)
        return

    if message.chat.type == 'private':
        # Process messages directly in private chats
        await process_messages(context, message)
    elif message.chat.type in ['group', 'supergroup']:
        # In groups, process only if bot is mentioned
        if is_bot_mentioned(context.bot.username, message):
            await process_messages(context, message)
    elif message.chat.type == 'channel':
        # TODO: Not sure what to do in channels. What is our behavior here?
        logger.warning("Received message in channel with chat ID %s", message.chat.id)
        message.reply_text("Channels are not currently supported")


async def leave_group(context: CallbackContext, message: Message) -> None:
    await context.bot.leave_chat(message.chat.id)
    logger.warning(
        f"Leaving non-whitelisted group with chat ID {message.chat.id}, "
        f"message type: {message.chat.type} and message: {message.text}"
    )


def is_blacklisted(message: Message) -> bool:
    return message.chat.id in Config.BLACKLISTED_GROUPS


def is_bot_mentioned(botname: str, message: Message) -> bool:
    return message and message.reply_to_message and f'@{botname}' in message.text


def is_youtube_url(url: str) -> bool:
    return 'youtube.com/watch' in url or 'youtu.be/' in url or 'youtube.com/shorts' in url


@track_function
async def process_messages(context: CallbackContext, message: Message) -> None:
    replied_message = message.reply_to_message if message.reply_to_message else message

    if replied_message.voice:
        handle_voice_message(context, replied_message)
    elif replied_message.text:
        await handle_text_message(context, replied_message)


@track_function
async def handle_voice_message(context: CallbackContext, message: Message) -> None:
    logger.info(f'New voice message from chat ID {message.chat.id} and user ID {message.from_user.id}({message.from_user.name})')

    progress_message = await message.reply_sticker(LISTENING_STICKER)

    file = await context.bot.get_file(message.voice.file_id)
    file_url = file.file_path

    transcription = await stt.transcribe_voice(file_url)
    await progress_message.delete()
    await message.reply_text(transcription, quote=True, parse_mode=ParseMode.HTML)


async def handle_text_message(context: CallbackContext, message: Message) -> None:
    # No change in the logic, just ensure it's properly awaited in the event loop
    logger.info(f'New text message from chat ID {message.chat.id} and user ID {message.from_user.id} ({message.from_user.name})')
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, message.text)

    if not urls:
        logger.warning(f'No URL found in message: {message.text}')
        return
    
    summary = None
    if is_youtube_url(urls[0]):
        await message.reply_sticker(WATCHING_STICKER)  # Assume this is an async operation
        summary = video_gpt.summarize(urls[0])
    else:
        await message.reply_sticker(READING_STICKER)  # Assume this is an async operation
        summary = article_gpt.summarize(urls[0])

    await message.reply_text(summary, quote=True, parse_mode=ParseMode.HTML)


@track_function
async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update '{update}' caused error '{type(context.error)}: {context.error}'")

    if not update:
        logger.error("No update found in error handler, can't surface error to the user.")
        return
    
    if not update.message:
        logger.error("No message found in update, can't surface error to the user. Update: {update}")
        return
    
    message = update.message
    await message.reply_html(_("Something went completely wrong"), quote=True)


@track_function
async def command_start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(_('Welcome message'), quote=True)
