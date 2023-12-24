from google.cloud import speech
from google.oauth2 import service_account

from bot.config import Config


class STT:
    def __init__(self, config: Config) -> None:
        service_file = config.get_google_service_file()
        credentials = service_account.Credentials.from_service_account_file(service_file)

        self._client = speech.SpeechClient(credentials=credentials)
        self._config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code="ru-RU",
            enable_word_confidence=True
        )

    async def transcribe_voice(self, voice_data: bytes) -> str:
        audio = speech.RecognitionAudio(content=voice_data)

        response = self._client.recognize(config=self._config, audio=audio)
        return ' '.join([result.alternatives[0].transcript for result in response.results])



