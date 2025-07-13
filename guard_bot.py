import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)

# Pull in your token via env → makes it safe on Render
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Only allow posting in this topic
ALLOWED_TOPIC = "💬 Trader Chat"
REMINDER_MESSAGE = "⚠️ This topic is read-only. Please post in 💬 Trader Chat only."

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def enforce_topic_restriction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.is_topic_message:
        return

    # bot's incoming Update gives you `msg.topic_name`
    if msg.topic_name != ALLOWED_TOPIC:
        try:
            await context.bot.delete_message(
                chat_id=msg.chat_id, message_id=msg.message_id
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

    # catch any plain-text message (not commands) and enforce our topic rule
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, enforce_topic_restriction)
    )

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
