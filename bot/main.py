import logging
import traceback

from commands import command_start, error_handler
from config import config
from log_config import setup_logging
from messages import BotBrain
from telegram import Update
from telegram.ext import CallbackContext, Application, ApplicationBuilder
import boto3
import asyncio
import json
from botocore.exceptions import NoCredentialsError

setup_logging()

logger = logging.getLogger(__name__)

# AWS stuff
sqs_client = boto3.client('sqs', region_name='us-west-2')

# Bot inits
bot_brain = BotBrain(config)


def pull_messages(sqs_queue_url) -> None:
    while True:
        try:
            # Visibility time and DLQ are set on infrastructure level.
            # See, CF template.
            response = sqs_client.receive_message(
                QueueUrl=sqs_queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
            )

            messages = response.get('Messages', [])
            logger.info(f'{len(messages)} message to process')

            for message in messages:
                logger.info(f"Received message: {message['Body']}")
                    
                first_decode = json.loads(message['Body'])
                final_dict = json.loads(first_decode)

                # Initialize Telegram bot application to keep backwards compatibility
                # TODO: reduce dependencies to Telegram classes
                application = ApplicationBuilder().token(config.get_telegram_token()).build()
                context = CallbackContext(application)
                update = Update.de_json(final_dict, application.bot)

                asyncio.run(bot_brain.process_new_message(update, context))

                # Delete the message from the queue to prevent reprocessing
                sqs_client.delete_message(
                    QueueUrl=sqs_queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        except Exception as e:
            logger.error(f"An error occurred: {e}\nCall stack: {traceback.format_exc()}")
            break

    
if __name__ == '__main__':
    pull_messages(config.get_message_queue_url())