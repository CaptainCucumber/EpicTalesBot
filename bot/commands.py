import logging

from localization import _
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(
        f"Update '{update}' caused error '{type(context.error)}: {context.error}'"
    )

    if not update:
        logger.error(
            "No update found in error handler, can't surface error to the user."
        )
        return

    if not update.message:
        logger.error(
            "No message found in update, can't surface error to the user. Update: {update}"
        )
        return

    message = update.message
    await message.reply_html(_("Something went completely wrong"), quote=True)


async def command_start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(_("Welcome message"), quote=True)
