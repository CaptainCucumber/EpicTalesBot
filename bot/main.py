import asyncio
import logging
from queue import Queue
from threading import Thread, current_thread

from config import config
from log_config import setup_logging
from messages import command_start, error_handler, handle_messages
from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackContext, CommandHandler,
                          MessageHandler, filters)

setup_logging()

logger = logging.getLogger(__name__)

message_queue = Queue()

def message_consumer(queue):
    loop = asyncio.new_event_loop()
    # it is important to set event loop here, I don't really understand why. I though asyncio still lives in the main thread
    asyncio.set_event_loop(loop) 
    while True:
        update, context = queue.get()
        if update is None and context is None: # Termination signal
            break

        logger.info(f"{current_thread().name} consumed {update}")

        loop.run_until_complete(handle_messages(update, context))
        queue.task_done()


async def message_router(update: Update, context: CallbackContext) -> None:
    message_queue.put((update, context))


def main() -> None:
    application = ApplicationBuilder().token(config.get_telegram_token()).build()

    application.add_handler(CommandHandler("start", command_start))
    application.add_handler(MessageHandler(filters.ALL, message_router))
    application.add_error_handler(error_handler)

    application.run_polling()

    
if __name__ == '__main__':
    consumers = []
    for _ in range(5):
        process = Thread(target=message_consumer, args=(message_queue,))
        process.start()
        consumers.append(process)

    main()
    logger.info("Cleaning resources....")

    # After the asyncio part completes, clean up the consumer processes
    for _ in range(5):  # Send termination signal
        message_queue.put((None, None))

    for consumer in consumers:
        consumer.join()

