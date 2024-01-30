import logging
import re
from typing import Optional

from article_gpt import ArticleGPT
from config import Config
from localization import _
from metrics import track_function
from stt import STT
from telegram import Message, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from video_gpt import VideoGPT
from __init__ import __version__

logger = logging.getLogger(__name__)


class BotBrain:
    READING_STICKER = "CAACAgEAAxkBAAPvZa08i8gvG70My_EEkqmhgwvLu5gAAqECAAKoyCFEr-C6Suk25ik0BA"
    WATCHING_STICKER = "CAACAgEAAxkBAAPzZa09iinK8z-W-mNnUp0YPHLDpkwAAhsCAAPUGESSRmhdQDpGTTQE"
    LISTENING_STICKER = "CAACAgEAAxkBAAP7Za1GmGxnW7OUXAy5-e6tIqgGZVwAAtcCAAKkdyBEDjNwiD91jjI0BA"

    def __init__(self, video_gpt_instance: VideoGPT, article_gpt_instance: ArticleGPT, stt_instance: Optional[STT]) -> None:
        self._video_gpt = video_gpt_instance
        self._article_gpt = article_gpt_instance
        self._stt = stt_instance

    def _is_blacklisted(self, message: Message) -> bool:
        return message.chat.id in Config.BLACKLISTED_GROUPS

    def _is_bot_mentioned(self, botname: str, message: Message) -> bool:
        return message and message.reply_to_message and f'@{botname}' in message.text

    def _is_youtube_url(self, url: str) -> bool:
        return 'youtube.com/watch' in url or 'youtu.be/' in url or 'youtube.com/shorts' in url

    async def _leave_group(self, context: CallbackContext, message: Message) -> None:
        await context.bot.leave_chat(message.chat.id)
        logger.warning(
            f"Leaving non-whitelisted group with chat ID {message.chat.id}, "
            f"message type: {message.chat.type} and message: {message.text}"
        )

    async def _route_message_by_type(self, context: CallbackContext, message: Message) -> None:
        replied_message = message.reply_to_message if message.reply_to_message else message

        if replied_message.voice:
            await self._handle_voice_message(context, replied_message)
        elif replied_message.text:
            await self._handle_text_message(context, replied_message)

    async def _handle_voice_message(self, context: CallbackContext, message: Message) -> None:
        logger.info(f'New voice message from chat ID {message.chat.id} and user ID {message.from_user.id} ({message.from_user.name})')

        progress_message = await message.reply_sticker(self.LISTENING_STICKER)

        file = await context.bot.get_file(message.voice.file_id)
        file_url = file.file_path

        transcription = await self._stt.transcribe_voice(file_url)
        await progress_message.delete()
        await message.reply_text(transcription, quote=True, parse_mode=ParseMode.HTML)

    async def _handle_text_message(self, context: CallbackContext, message: Message) -> None:
        logger.info(f'New text message from chat ID {message.chat.id} and user ID {message.from_user.id} ({message.from_user.name})')
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message.text)

        if not urls:
            logger.warning(f'No URL found in message: {message.text}')
            return
        
        summary = None
        progress_message = None
        if self._is_youtube_url(urls[0]):
            logger.info(f"Summarizing video: {urls[0]}")
            progress_message = await message.reply_sticker(self.WATCHING_STICKER)
            summary = self._video_gpt.summarize(urls[0])
        else:
            logger.info(f"Summarizing article: {urls[0]}")
            progress_message = await message.reply_sticker(self.READING_STICKER)
            summary = self._article_gpt.summarize(urls[0])

        await progress_message.delete()
        await message.reply_text(summary, quote=True, parse_mode=ParseMode.HTML)

    async def _handle_command(self, context: CallbackContext, message: Message) -> None:
        logger.info(f"New command '{message.text}' from chat ID {message.chat.id} and user ID {message.from_user.id} ({message.from_user.name})")
        command = message.text.split()[0]

        if command == '/start':
            await message.reply_html(_('Welcome message'), quote=True)
        elif command == '/version':
            await message.reply_html(f'<code>{__version__}</code>')
        else:
            logger.info(f"Unknown command '{command}' from user {message.from_user.id} ({message.from_user.name})")


    @track_function
    async def process_new_message(self, update: Update, context: CallbackContext, botname: Optional[str]) -> None:
        try:
            message = update.message if update.message else update.channel_post

            if not message:
                logger.warning("Received message with no content")
                return

            if self._is_blacklisted(message):
                self._leave_group(context, message)
                return

            logger.info(f"Processing new message with type: '{message.chat.type}'")
            if message.text.startswith('/'):
                await self._handle_command(context, message)
            elif message.chat.type == 'private':
                # Process messages directly in private chats
                await self._route_message_by_type(context, message)
            elif message.chat.type in ['group', 'supergroup']:
                # In groups, process only if bot is mentioned
                if self._is_bot_mentioned(botname, message):
                    await self._route_message_by_type(context, message)
                else:
                    logger.info("The bot name was not mentioned in the message")
            elif message.chat.type == 'channel':
                # TODO: Not sure what to do in channels. What is our behavior here?
                logger.warning("Received message in channel with chat ID %s", message.chat.id)
                message.reply_text("Channels are not currently supported")
        except Exception as e:
            # TODO: Need to report back to user that something went wrong
            logger.error(f"Error processing message: {update}", exc_info=e, stack_info=True)

