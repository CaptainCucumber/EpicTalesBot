import requests
import openai
from pydub import AudioSegment
import io
import whisper
from config import Config
import tempfile
import os

class STT:
    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self.whisper_model = whisper.load_model("base")  # Load Whisper model

    def _download_audio(self, voice_file_id: str) -> bytes:
        response = requests.get(voice_file_id)
        return response.content

    def _convert_oga_to_wav(self, oga_audio_data: bytes) -> io.BytesIO:
        oga_audio_stream = io.BytesIO(oga_audio_data)
        audio = AudioSegment.from_ogg(oga_audio_stream)

        wav_audio_stream = io.BytesIO()
        audio.export(wav_audio_stream, format="wav")
        wav_audio_stream.seek(0)

        return wav_audio_stream

    async def transcribe_voice(self, url: str) -> str:
        voice_data = self._download_audio(url)

        # Convert OGA to WAV
        wav_audio_stream = self._convert_oga_to_wav(voice_data)

        # Save the WAV audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(wav_audio_stream.read())
            temp_file_path = temp_file.name

        # Transcribe using Whisper
        audio_data = whisper.load_audio(temp_file_path)
        result = self.whisper_model.transcribe(audio_data)
        voice_text = result["text"]

        # Clean up: delete the temporary file
        os.remove(temp_file_path)

        return voice_text