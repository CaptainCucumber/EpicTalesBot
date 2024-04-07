import io
import logging
import time
import uuid

import boto3
import requests
from config import Config
from metrics import publish_voice_message_processed
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AWSTranscribe:
    _MAX_VOICE_AUDIO_LENGTH = 5 * 60  # 5 minutes in seconds

    def __init__(self, config: Config) -> None:
        self._transcribe_client = boto3.client(
            "transcribe", region_name=config.aws_region
        )
        self._s3_client = boto3.client("s3", region_name=config.aws_region)
        self._bucket_name = config.aws_audio_transcribe_bucket_name

    def _upload_audio_to_s3(self, audio_bytes: bytes, file_name: str) -> str:
        self._s3_client.put_object(
            Body=audio_bytes, Bucket=self._bucket_name, Key=file_name
        )
        return f"s3://{self._bucket_name}/{file_name}"

    def _download_audio(self, voice_file_url: str) -> bytes:
        response = requests.get(voice_file_url)
        return response.content

    def transcribe_voice(self, url: str) -> (str, float):
        voice_data = self._download_audio(url)
        oga_audio_stream = io.BytesIO(voice_data)
        audio = AudioSegment.from_ogg(oga_audio_stream)

        original_duration = audio.duration_seconds
        logger.info(f"Audio duration: {original_duration} seconds")

        audio = audio[: self._MAX_VOICE_AUDIO_LENGTH * 1000]
        file_name = f"{uuid.uuid4()}.ogg"
        s3_uri = self._upload_audio_to_s3(voice_data, file_name)

        job_name = str(uuid.uuid4())
        self._transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": s3_uri},
            MediaFormat="ogg",
            LanguageCode="ru-RU",
            Settings={
                "ShowSpeakerLabels": False,
                "ChannelIdentification": False,
            },
        )

        start_time = time.time()
        while True:
            status = self._transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            if status["TranscriptionJob"]["TranscriptionJobStatus"] in [
                "COMPLETED",
                "FAILED",
            ]:
                break
            time.sleep(5)

        transcript_uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_response = requests.get(transcript_uri)
        transcript_text = transcript_response.json()["results"]["transcripts"][0][
            "transcript"
        ]

        end_time = time.time()
        publish_voice_message_processed(
            "aws", original_duration, audio.duration_seconds, end_time - start_time
        )
        return transcript_text, original_duration
