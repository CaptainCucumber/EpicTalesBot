import io
import logging

import openai
import requests
from config import Config
from faster_whisper import WhisperModel
from localization import _
from metrics import publish_voice_message_processed
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class STT:
    _MAX_VOICE_AUDIO_LENGTH = 5 * 60

    def __init__(self, config: Config, location: str) -> None:
        openai.api_key = config.get_open_ai_key()
        self.location = location

        model_cache_dir = "/var/cache/epictales/faster-whisper/" + location

        if location == "gpu":
            self.model = WhisperModel(
                "large-v3",
                device="cuda",
                compute_type="float16",
                download_root=model_cache_dir,
            )
        elif location == "cpu":
            self.model = WhisperModel(
                "large-v3",
                device="cpu",
                cpu_threads=12,
                num_workers=12,
                download_root=model_cache_dir,
            )
        else:
            raise Exception(f"Unknown location for the model: {location}")

    def _download_audio(self, voice_file_id: str) -> bytes:
        response = requests.get(voice_file_id)
        return response.content

    def transcribe_voice(self, url: str) -> str:
        voice_data = self._download_audio(url)

        oga_audio_stream = io.BytesIO(voice_data)
        audio = AudioSegment.from_ogg(oga_audio_stream)

        original_duration = audio.duration_seconds
        audio = audio[: self._MAX_VOICE_AUDIO_LENGTH * 1000]

        logger.info(f"Audio duration: {original_duration} seconds")
        wav_audio_stream = io.BytesIO()
        audio.export(wav_audio_stream, format="wav")
        wav_audio_stream.seek(0)

        # Transcribe using Whisper
        segments, info = self.model.transcribe(wav_audio_stream, beam_size=5)

        publish_voice_message_processed(
            "local" if self.location == "gpu" else "cpu",
            original_duration,
            audio.duration_seconds,
        )

        return "".join(segment.text for segment in segments), original_duration
