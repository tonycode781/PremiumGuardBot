import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load your bot token from the environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Only this thread is writable
ALLOWED_THREAD_ID = 7
REMINDER_MESSAGE = "⚠️ This topic is read-only. Please post in 💬 Trader Chat only."

# Standard logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def enforce_topic_restriction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or msg.message_thread_id is None:
        return

    # DEBUG: log each thread so you can confirm
    logger.info("Received in thread_id=%s: %s", msg.message_thread_id, msg.text)

    if msg.message_thread_id != ALLOWED_THREAD_ID:
        try:
            await context.bot.delete_message(
                chat_id=msg.chat_id,
                message_id=msg.message_id,
            )
            await context.bot.send_message(
                chat_id=msg.chat_id,
                text=REMINDER_MESSAGE,
                message_thread_id=msg.message_thread_id,
            )
        except Exception as e:
            logger.error("Failed to enforce topic restriction: %s", e)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, enforce_topic_restriction)
    )

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
