from settings.chat_settings_repository import ChatSettingsRepository


class ChatSettings:
    def __init__(self, chat_id: int):
        self.repository = ChatSettingsRepository("ChatSettings")
        self.settings = self.repository.get_chat_settings(chat_id)
