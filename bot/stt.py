import io
import logging
import os
import tempfile

import openai
import requests
import whisper
from config import Config
from pydub import AudioSegment

logger = logging.getLogger(__name__)

class STT:
    _STT_CONTEXTUALIZATION_PROMPT = "contextualization_prompt.txt"
    _MAX_VOICE_AUDIO_LENGTH = 60

    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self.whisper_model = whisper.load_model("small")
        self._prompt_content = None

    def _gpt_prompt(self) -> str:
        if self._prompt_content is None:
            file_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(file_dir, self._STT_CONTEXTUALIZATION_PROMPT)
        
            with open(file_path, 'r', encoding='utf-8') as file:
                self._prompt_content = file.read()

        return self._prompt_content

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

    async def transcribe_voice(self, url: str) -> str:
        voice_data = self._download_audio(url)

        # Convert OGA to WAV
        wav_audio_stream, reduced = self._convert_oga_to_wav(voice_data)

        # Save the WAV audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(wav_audio_stream.read())
            temp_file_path = temp_file.name

        # Transcribe using Whisper
        audio_data = whisper.load_audio(temp_file_path)
        result = self.whisper_model.transcribe(audio_data, condition_on_previous_text=False)
        voice_text = result["text"]

        # Clean up: delete the temporary file
        os.remove(temp_file_path)

        if reduced:
            voice_text = voice_text + "\n\n__*Только первые 60 секунд переведены.*__"
        
        return voice_text