import io
import json
import logging

import requests
from config import Config
from google.cloud import speech
from google.oauth2 import service_account
from localization import _
from metrics import publish_voice_message_processed
from pydub import AudioSegment
from pydub.utils import mediainfo

logger = logging.getLogger(__name__)


class GoogleSTT:
    _MAX_VOICE_AUDIO_LENGTH = 5 * 60

    def __init__(self, config: Config) -> None:
        with open(config.get_google_cloud_creds_file(), "r") as file:
            credentials_json = json.loads(file.read())
            credentials = service_account.Credentials.from_service_account_info(
                credentials_json
            )
            self._client = speech.SpeechClient(credentials=credentials)

    def _download_audio(self, voice_file_id: str) -> bytes:
        response = requests.get(voice_file_id)
        return response.content

    async def transcribe_voice(self, url: str) -> str:
        voice_data = self._download_audio(url)

        oga_audio_stream = io.BytesIO(voice_data)
        audio = AudioSegment.from_ogg(oga_audio_stream)

        original_duration = audio.duration_seconds
        logger.info(f"Audio duration: {original_duration} seconds")

        audio = audio[: self._MAX_VOICE_AUDIO_LENGTH * 1000]
        frame_rate = audio.frame_rate

        # Configure the request
        speech_audio = speech.RecognitionAudio(content=voice_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=frame_rate,
            language_code="ru-RU",
            alternative_language_codes=["ru-RU", "uk-UA", "en-US"],
            enable_word_confidence=True,
            enable_automatic_punctuation=True,
            profanity_filter=False,
            use_enhanced=True,
            model="default",
        )

        # Transcribe the audio file
        response = self._client.recognize(config=config, audio=speech_audio)

        publish_voice_message_processed(
            "cloud", original_duration, audio.duration_seconds
        )
        return (
            " ".join(
                [result.alternatives[0].transcript for result in response.results]
            ),
            original_duration,
        )
