import argparse
import asyncio
import json
import logging
import traceback

import boto3
import requests
from article_gpt import ArticleGPT
from config import config
from google_stt import GoogleSTT
from log_config import setup_logging
from messages import BotBrain
from metrics import publish_process_start_command_used
from stt import STT
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CallbackContext
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
    "--disable-stt", action="store_true", help="Disable Speech-to-text functionality."
)
parser.add_argument(
    "--message-queue", type=str, required=True, help="Queue URL to pull messages from"
)
args = parser.parse_args()

# Bot initialization
stt_instance = None if args.disable_stt else STT(config)
gstt_instance = GoogleSTT(config)
video_gpt_instance = VideoGPT(config)
article_gpt_instance = ArticleGPT(config)
bot_brain = BotBrain(
    video_gpt_instance, article_gpt_instance, stt_instance, gstt_instance
)

logger.info(f"The bot is initialized. Speech-to-text disabled? {args.disable_stt}")


def get_bot_username(bot_token) -> str:
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        bot_info = response.json()
        return bot_info["result"]["username"]
    return None


def pull_messages(sqs_queue_url) -> None:
    logger.info(f"Start pulling messages from: {sqs_queue_url}")

    while True:
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
                final_dict = json.loads(first_decode)

                # Initialize Telegram bot application to keep backwards compatibility
                # TODO: reduce dependencies to Telegram classes
                application = (
                    ApplicationBuilder().token(config.get_telegram_token()).build()
                )
                context = CallbackContext(application)

                bot_username = get_bot_username(config.get_telegram_token())

                update = Update.de_json(
                    final_dict, Bot(token=config.get_telegram_token())
                )

                asyncio.run(
                    bot_brain.process_new_message(update, context, bot_username)
                )

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
    publish_process_start_command_used()
    pull_messages(args.message_queue)
