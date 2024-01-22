import io
import logging
import os
import tempfile

import openai
import requests
from faster_whisper import WhisperModel
from config import Config
from localization import _
from metrics import track_function
from pydub import AudioSegment

logger = logging.getLogger(__name__)

class STT:
    _MAX_VOICE_AUDIO_LENGTH = 5*60

    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self.model = WhisperModel("large-v2", device="cuda", compute_type="float16")

    def _download_audio(self, voice_file_id: str) -> bytes:
        response = requests.get(voice_file_id)
        return response.content

    def _convert_oga_to_wav(self, oga_audio_data: bytes) -> tuple[io.BytesIO, bool]:
        oga_audio_stream = io.BytesIO(oga_audio_data)
        audio = AudioSegment.from_ogg(oga_audio_stream)

        logger.info(f"Audio duration: {audio.duration_seconds} seconds")

        wav_audio_stream = io.BytesIO()
        audio[:self._MAX_VOICE_AUDIO_LENGTH * 1000].export(wav_audio_stream, format="wav")
        wav_audio_stream.seek(0)

        return wav_audio_stream, audio.duration_seconds > self._MAX_VOICE_AUDIO_LENGTH

    @track_function
    async def transcribe_voice(self, url: str) -> str:
        voice_data = self._download_audio(url)

        # Convert OGA to WAV
        wav_audio_stream, reduced = self._convert_oga_to_wav(voice_data)

        # Transcribe using Whisper
        segments, info  = self.model.transcribe(wav_audio_stream, beam_size=5)
        result = ''.join(segment.text for segment in segments)
        voice_text = f'<i>{result}</i>'

        if reduced:
            message = _("The translation is limited to the first 60 seconds.")
            voice_text = f"{voice_text}\n\n<b>{message}</b>"
        
        return voice_text