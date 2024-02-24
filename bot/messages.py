import logging
import re
from typing import Union

from __init__ import __version__
from article_gpt import ArticleGPT
from config import config
from google_stt import GoogleSTT
from localization import _
from metrics import (
    publish_articles_summarized,
    publish_request_success_rate,
    publish_start_command_used,
    publish_unknown_command_used,
    publish_version_command_used,
    publish_videos_watched,
)
from models.message import Message
from settings.chat_settings import ChatSettings
from stt import STT
from tlg.api import TelegramAPI
from touch import Touch
from tracking import generate_tracking_container
from video_gpt import VideoGPT

logger = logging.getLogger(__name__)


class MessageDispatcher:
    MAX_MESSAGE_LENGTH = 4096

    READING_STICKER = (
        "CAACAgEAAxkBAAPvZa08i8gvG70My_EEkqmhgwvLu5gAAqECAAKoyCFEr-C6Suk25ik0BA"
    )
    WATCHING_STICKER = (
        "CAACAgEAAxkBAAPzZa09iinK8z-W-mNnUp0YPHLDpkwAAhsCAAPUGESSRmhdQDpGTTQE"
    )
    LISTENING_STICKER = (
        "CAACAgEAAxkBAAP7Za1GmGxnW7OUXAy5-e6tIqgGZVwAAtcCAAKkdyBEDjNwiD91jjI0BA"
    )

    def __init__(
        self,
        botname: str,
        video_gpt_instance: VideoGPT,
        article_gpt_instance: ArticleGPT,
        voice_transcriber: Union[STT, GoogleSTT],
        update: Message,
    ) -> None:
        self._botname = botname
        self._video_gpt = video_gpt_instance
        self._article_gpt = article_gpt_instance
        self._stt = voice_transcriber
        self._update = update

        self._telegram = TelegramAPI(config)

        self._touch = Touch("./touchdir")

        self._progress_message = None

    @property
    def user_id(self) -> int:
        return self._update.message.from_user.id

    @property
    def chat_id(self) -> int:
        return self._update.message.chat.id

    @property
    def chat_type(self) -> str:
        return self._update.message.chat.type

    @property
    def username(self) -> str:
        return (
            self._update.message.from_user.username
            if "username" in self._update.message.from_user
            else "XXX_NO_USERNAME"
        )

    @property
    def is_group(self) -> bool:
        return self.chat_type in ["supergroup", "group"]

    @property
    def message_id(self) -> int:
        return self._update.message.message_id

    def _is_bot_mentioned(self, botname: str, message: dict) -> bool:
        return f"@{botname}" in message.text

    def _is_youtube_url(self, url: str) -> bool:
        return (
            "youtube.com/watch" in url
            or "youtu.be/" in url
            or "youtube.com/shorts" in url
        )

    def _handle_voice_message(self, message: Message) -> None:

        def split_and_format_string(input_string, max_length):
            parts = [
                input_string[i : i + max_length]
                for i in range(0, len(input_string), max_length)
            ]
            formatted_parts = ["<i>{}</i>".format(part) for part in parts]
            return formatted_parts

        logger.info(
            f"New voice message from chat ID {self.chat_id} and user ID {self.user_id} ({self.username})"
        )

        self._progress_message = self._telegram.reply_with_sticker_safe(
            self.chat_id, self.message_id, self.LISTENING_STICKER
        )

        file_url = self._telegram.get_voice_file_path(message.voice.file_id)

        transcription, duration = self._stt.transcribe_voice(file_url)
        texts = split_and_format_string(transcription, self.MAX_MESSAGE_LENGTH)

        if "message_id" in self._progress_message:
            self._telegram.delete_message_safe(
                self.chat_id, self._progress_message["message_id"]
            )

        for text in texts:
            self._telegram.reply_message(self.chat_id, message.message_id, text)

        if duration > self._stt._MAX_VOICE_AUDIO_LENGTH:
            limit_message = _("The translation is limited to the first 60 seconds.")
            warning_message = f"<b>{limit_message}</b>"
            self._telegram.reply_message(self.chat_id, self.message_id, warning_message)

        publish_request_success_rate(1, True)

    def _handle_text_message(self, message: dict) -> None:
        logger.info(
            f"New text message from chat ID {self.chat_id} and user ID {self.user_id} ({self.username})"
        )
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, message.text)

        if not urls:
            logger.warning(f"No URL found in message: {message.text}")
            return

        summary = None
        is_youtube = self._is_youtube_url(urls[0])
        if is_youtube:
            logger.info(f"Summarizing video: {urls[0]}")
            self._progress_message = self._telegram.reply_with_sticker_safe(
                self.chat_id, self.message_id, self.WATCHING_STICKER
            )
            summary = self._video_gpt.summarize(urls[0])
        else:
            logger.info(f"Summarizing article: {urls[0]}")
            self._progress_message = self._telegram.reply_with_sticker_safe(
                self.chat_id, self.message_id, self.READING_STICKER
            )
            summary = self._article_gpt.summarize(urls[0])

        if "message_id" in self._progress_message:
            self._telegram.delete_message_safe(
                self.chat_id, self._progress_message["message_id"]
            )

        self._telegram.reply_message(self.chat_id, self.message_id, summary)

        publish_videos_watched() if is_youtube else publish_articles_summarized()
        publish_request_success_rate(1, True)

    def _handle_command(
        self, chat_settings: ChatSettings, command: str, message: Message
    ) -> None:
        logger.info(
            f"New command '{command}' from chat ID {self.chat_id} and user ID {self.user_id} ({self.username})"
        )

        if command == "/start":
            if not chat_settings:
                chat_settings.initialize()

            self._telegram.reply_message(
                self.chat_id, self.message_id, _("Welcome message")
            )
            publish_start_command_used()
        elif command == "/version":
            self._telegram.reply_message(
                self.chat_id, self.message_id, f"<code>{__version__}</code>"
            )
            publish_version_command_used()

        elif command == "/listen":
            if "reply_to_message" in message and "voice" in message.reply_to_message:
                self._handle_voice_message(message.reply_to_message)
            else:
                self._telegram.reply_message(
                    self.chat_id, self.message_id, _("No voice message to transcribe")
                )
        else:
            logger.info(
                f"Unknown command '{command}' from user {self.user_id} ({self.username})"
            )
            publish_unknown_command_used()

    def _get_command(self, message_text: str) -> bool:
        if not message_text.startswith("/"):
            return None

        return message_text.split()[0]

    def _get_voice_message(self, message: dict) -> bool:
        if "voice" in message:
            return message

        return {}

    def _send_new_settings_message(self) -> None:
        self._telegram.send_message(self.chat_id, _("New settings in tact"))
        self._touch.touch_entity(self.chat_id, "new_settings")

    def process_new_message(self) -> None:
        try:
            if "message" not in self._update:
                logger.error(
                    "No message in update. Don't know how to process the update"
                )
                return

            message = self._update.message
            generate_tracking_container(
                user_id=None if message.from_user.id is None else message.from_user.id,
                chat_id=message.chat.id,
                chat_type=message.chat.type,
            )

            chat_settings = ChatSettings(self.chat_id)
            text = message.get("text", {})
            if text:
                # Handle commands
                command = self._get_command(message.text)
                if command:
                    self._handle_command(chat_settings, command, message)
                    return

            if not chat_settings:
                self._send_new_settings_message()
                chat_settings.initialize()

            # Autotranscibe is "on" see if there is a voice message
            if "voice" in message and chat_settings.autotranscribe:
                self._handle_voice_message(message)
                return

            # TODO: if user adds the bot to a channel, sent the warning message
        except Exception as e:
            # TODO: Need to report back to user that something went wrong
            publish_request_success_rate(1, False)
            logger.error(
                f"Error processing message: {self._update}", exc_info=e, stack_info=True
            )

            if self._progress_message and "message_id" in self._progress_message:
                logger.info(
                    "Clearning progress message that was left in chat due to exception."
                )
                self._telegram.delete_message_safe(
                    self.chat_id, self._progress_message["message_id"]
                )
