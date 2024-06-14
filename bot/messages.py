import logging
import re
from typing import Optional, Union

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
from tracking import generate_tracking_container
from video_gpt import VideoGPT

logger = logging.getLogger(__name__)


def get_first_link_from_message(message: Message) -> Optional[str]:
    if "text" not in message:
        return None

    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, message.text)
    if not urls:
        return None

    return urls[0]


def get_video_link_from_message(message: Message) -> Optional[str]:
    link = get_first_link_from_message(message)

    if not link:
        return None

    if (
        "youtube.com/watch" in link
        or "youtu.be/" in link
        or "youtube.com/shorts" in link
        or "youtube.com/live" in link
    ):
        return link

    return None


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
        self._message = self._update.message

        self._telegram = TelegramAPI(config)

        self._progress_message = None
        generate_tracking_container(
            user_id=(
                None
                if self._message.from_user.id is None
                else self._message.from_user.id
            ),
            chat_id=self._message.chat.id,
            chat_type=self._message.chat.type,
        )

    @property
    def user_id(self) -> int:
        return self._message.from_user.id

    @property
    def chat_id(self) -> int:
        return self._message.chat.id

    @property
    def chat_type(self) -> str:
        return self._message.chat.type

    @property
    def username(self) -> str:
        return (
            self._message.from_user.username
            if "username" in self._message.from_user
            else "XXX_NO_USERNAME"
        )

    @property
    def is_group(self) -> bool:
        return self.chat_type in ["supergroup", "group"]

    @property
    def message_id(self) -> int:
        return self._message.message_id

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

    def _summarize_video(self, link: str, message: Message) -> None:
        logger.info(f"Summarizing video: {link}")

        self._progress_message = self._telegram.reply_with_sticker_safe(
            self.chat_id, message.message_id, self.WATCHING_STICKER
        )
        summary = self._video_gpt.summarize(link)

        if "message_id" in self._progress_message:
            self._telegram.delete_message_safe(
                self.chat_id, self._progress_message["message_id"]
            )

        self._telegram.reply_message(self.chat_id, message.message_id, summary)

        publish_videos_watched()
        publish_request_success_rate(1, True)

    def _summarize_article(self, link: str, message: Message) -> None:
        logger.info(f"Summarizing article: {link}")

        self._progress_message = self._telegram.reply_with_sticker_safe(
            self.chat_id, message.message_id, self.READING_STICKER
        )
        summary = self._article_gpt.summarize(link)

        if "message_id" in self._progress_message:
            self._telegram.delete_message_safe(
                self.chat_id, self._progress_message["message_id"]
            )

        self._telegram.reply_message(self.chat_id, message.message_id, summary)

        publish_articles_summarized()
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
            return

        elif command == "/version":
            self._telegram.reply_message(
                self.chat_id, self.message_id, f"<code>{__version__}</code>"
            )
            publish_version_command_used()
            return

        elif command == "/listen":
            if "reply_to_message" in message and "voice" in message.reply_to_message:
                self._handle_voice_message(message.reply_to_message)
            else:
                self._telegram.reply_message(
                    self.chat_id, self.message_id, _("No voice message to transcribe")
                )
            return

        elif command == "/read":
            link = get_first_link_from_message(message)
            if link:
                self._summarize_article(link, message)
                return

            logger.info(
                f"No URL found in message: {message.text}. See if reply exist and there is a link there."
            )

            link = get_first_link_from_message(message.get("reply_to_message", {}))
            if link:
                self._summarize_article(link, message.reply_to_message)
                return

            self._telegram.reply_message(
                self.chat_id, self.message_id, _("No article to summarize")
            )
            return
        elif command == "/watch":
            link = get_video_link_from_message(message)
            if link:
                self._summarize_video(link, message)
                return

            link = get_video_link_from_message(message.get("reply_to_message", {}))
            if link:
                self._summarize_video(link, message.reply_to_message)
                return

            self._telegram.reply_message(
                self.chat_id, self.message_id, _("No video to summarize")
            )
            return

        elif command == "/autotranscribe":
            if not chat_settings:
                chat_settings.initialize()

            chat_settings.autotranscribe = not chat_settings.autotranscribe

            message = (
                _("Auto-transcribe enabled")
                if chat_settings.autotranscribe
                else _("Auto-transcribe disabled")
            )
            self._telegram.reply_message(self.chat_id, self.message_id, message)
            return

        else:
            logger.info(
                f"Unknown command '{command}' from user {self.user_id} ({self.username})"
            )
            publish_unknown_command_used()

    def _get_command(self, message_text: str) -> bool:
        if not message_text.startswith("/"):
            return None

        command = message_text.split()[0]
        if command.endswith(self._botname):
            return command.split("@")[0]

        return command

    def _get_voice_message(self, message: dict) -> bool:
        if "voice" in message:
            return message

        return {}

    def _send_new_settings_message(self) -> None:
        self._telegram.send_message(self.chat_id, _("New settings in tact"))

    def process_new_message(self) -> None:
        try:
            chat_settings = ChatSettings(self.chat_id)
            text = self._message.get("text", {})
            if text:
                # Handle commands
                command = self._get_command(self._message.text)
                if command:
                    if not chat_settings:
                        self._send_new_settings_message()
                        chat_settings.initialize()

                    self._handle_command(chat_settings, command, self._message)
                    return

            if not chat_settings:
                self._send_new_settings_message()
                chat_settings.initialize()

            # Autotranscibe is "on" see if there is a voice message
            if "voice" in self._message and chat_settings.autotranscribe:
                self._handle_voice_message(self._message)
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
