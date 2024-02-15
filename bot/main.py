import argparse
import json
import logging
import signal
import sys
import traceback

import boto3
import requests
from article_gpt import ArticleGPT
from config import config
from google_stt import GoogleSTT
from log_config import setup_logging
from messages import MessageDispatcher
from metrics import publish_process_started
from models.message import Message
from stt import STT
from video_gpt import VideoGPT

setup_logging()
logger = logging.getLogger(__name__)

# AWS stuff
sqs_client = boto3.client(
    "sqs",
    region_name=config.get_aws_region(),
    aws_access_key_id=config.get_aws_access_key_id(),
    aws_secret_access_key=config.get_aws_secret_access_key(),
)

# Command line arguments parsing
parser = argparse.ArgumentParser(description="EpicTales bot")
parser.add_argument(
    "--processing-voice",
    type=str,
    choices=["cpu", "gpu", "cloud"],
    default="gpu",
    help="Set where voice messages should be processed: on local CPU, local GPU, or Cloud.",
)
parser.add_argument(
    "--message-queue", type=str, required=True, help="Queue URL to pull messages from"
)
args = parser.parse_args()

# Add a global flag for shutdown
shutdown_flag = False


def signal_handler(signum, frame):
    global shutdown_flag
    logger.info("Receive terminate signal. Shutting down...")
    shutdown_flag = True


# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Bot initialization
stt_instance = None
if args.processing_voice == "cpu":
    logger.info("Using local CPU for speech-to-text")
    stt_instance = STT(config, "cpu")
elif args.processing_voice == "gpu":
    logger.info("Using local GPU for speech-to-text")
    stt_instance = STT(config, "gpu")
elif args.processing_voice == "cloud":
    stt_instance = GoogleSTT(config)
else:
    raise Exception(f"Unknown location for the model: {args.processing_voice}")

video_gpt_instance = VideoGPT(config)
article_gpt_instance = ArticleGPT(config)

logger.info(f"The bot is initialized. Speech-to-text runs on '{args.processing_voice}'")


def get_bot_username(bot_token) -> str:
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        bot_info = response.json()
        return bot_info["result"]["username"]
    return None


def pull_messages(sqs_queue_url) -> None:
    global shutdown_flag

    logger.info(f"Start pulling messages from: {sqs_queue_url}")
    botname = get_bot_username(config.get_telegram_token())

    while not shutdown_flag:
        try:
            # Visibility time and DLQ are set on infrastructure level.
            # See, CF template.
            response = sqs_client.receive_message(
                QueueUrl=sqs_queue_url,
                AttributeNames=["All"],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
            )

            messages = response.get("Messages", [])

            for message in messages:
                logger.info("Receive new message from the queue")

                first_decode = json.loads(message["Body"])
                update = json.loads(first_decode)

                bot_brain = MessageDispatcher(
                    botname,
                    video_gpt_instance,
                    article_gpt_instance,
                    stt_instance,
                    Message(update),
                )

                bot_brain.process_new_message()

                # Delete the message from the queue to prevent reprocessing
                sqs_client.delete_message(
                    QueueUrl=sqs_queue_url, ReceiptHandle=message["ReceiptHandle"]
                )
        except Exception as e:
            if message and "Body" in message:
                logger.error(f"Received message: {message['Body']}")

            logger.error(
                f"An error occurred: {e}\nCall stack: {traceback.format_exc()}"
            )
            break


if __name__ == "__main__":
    publish_process_started()
    pull_messages(args.message_queue)

    logger.info("Service shutdown completed. Bye!")
