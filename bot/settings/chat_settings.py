from settings.chat_settings_repository import ChatSettingsRepository


class ChatSettings:
    def __init__(self, chat_id: int):
        self._chat_id = chat_id
        self._repository = ChatSettingsRepository("ChatSettings")
        self._settings = self._repository.get_chat_settings(self._chat_id)

    def __bool__(self):
        return bool(self._settings)

    def initialize(self) -> None:
        if self._settings:
            raise Exception("Settings already initialized")

        self._settings = {"autotranscribe": False}
        self._repository.update_chat_settings(self._chat_id, self._settings)

    @property
    def autotranscribe(self) -> bool:
        return self._settings["autotranscribe"]

    @autotranscribe.setter
    def autotranscribe(self, value: bool) -> None:
        self._settings["autotranscribe"] = value
        self._repository.update_chat_settings(self._chat_id, self._settings)
