import json
import logging

import requests
from config import Config
from tlg.record import RecordRepository

logger = logging.getLogger(__name__)


class TelegramAPI:
    def __init__(self, config: Config) -> int:
        self.base_url = f"https://api.telegram.org/bot{config.telegram_token}/"
        self.file_base_url = (
            f"https://api.telegram.org/file/bot{config.telegram_token}/"
        )
        self.record_repository = RecordRepository(config.environment + "-Records")

    def reply_message(self, chat_id: int, message_id: int, text: str) -> dict:
        """Replies to an existing message in a chat in HTML parse mode."""
        method = "sendMessage"
        url = self.base_url + method
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "reply_to_message_id": message_id,
        }
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(f"Failed to send message: {response.text}")

        result = json.loads(response.text)["result"]
        update_id = int(f"{result['chat']['id']}{result['message_id']}")
        self.record_repository.put_record(update_id, result)
        return result

    def reply_with_sticker(self, chat_id: int, message_id: int, sticker: str) -> dict:
        """Sends a sticker in reply to a message."""
        method = "sendSticker"
        url = self.base_url + method
        data = {
            "chat_id": chat_id,
            "sticker": sticker,
            "reply_to_message_id": message_id,
        }
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(f"Failed to send sticker: {response.text}")

        result = json.loads(response.text)["result"]
        return result

    def reply_with_sticker_safe(
        self, chat_id: int, message_id: int, sticker: str
    ) -> dict:
        """Replies with a sticker in a safe manner by catching and logging any exceptions."""
        result = dict()
        try:
            result = self.reply_with_sticker(chat_id, message_id, sticker)
        except Exception as e:
            logger.error(f"Failed to send sticker: {e}")

        return result

    def delete_message(self, chat_id: int, message_id: int) -> None:
        """Deletes a message."""
        method = "deleteMessage"
        url = self.base_url + method
        data = {"chat_id": chat_id, "message_id": message_id}
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(f"Failed to delete message: {response.text}")

    def delete_message_safe(self, chat_id: int, message_id: int) -> None:
        """Deletes a message in a safe manner by catching and logging any exceptions."""
        try:
            self.delete_message(chat_id, message_id)
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")

    def get_voice_file_path(self, file_id: str) -> str:
        """Retrieves the full file path to a voice message using its file_id."""
        method = "getFile"
        url = self.base_url + method
        params = {"file_id": file_id}
        response = requests.get(url, params=params)
        if not response.ok:
            raise Exception(f"Failed to get file information: {response.text}")

        file_path = json.loads(response.text)["result"]["file_path"]
        full_file_path = self.file_base_url + file_path
        return full_file_path

    def send_message_with_inline_keyboard(
        self, chat_id: int, text: str, keyboard: list
    ) -> dict:
        """Sends a message with an inline keyboard."""
        method = "sendMessage"
        url = self.base_url + method
        reply_markup = {"inline_keyboard": keyboard}
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(reply_markup),
        }
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(
                f"Failed to send message with inline keyboard: {response.text}"
            )

        result = json.loads(response.text)["result"]
        return result

    def answer_callback_query(
        self, callback_query_id: str, text: str = "", show_alert: bool = False
    ) -> dict:
        """Sends an answer to a callback query, optionally with an alert."""
        method = "answerCallbackQuery"
        url = self.base_url + method
        data = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert,
        }
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(f"Failed to answer callback query: {response.text}")

        result = json.loads(response.text)
        return result

    def send_message(self, chat_id: int, text: str) -> dict:
        """Sends a message to a chat in HTML parse mode."""
        method = "sendMessage"
        url = self.base_url + method
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(f"Failed to send message: {response.text}")

        result = json.loads(response.text)["result"]
        return result
