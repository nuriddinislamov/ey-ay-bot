from telegram.ext import Application, CommandHandler
import os
import dotenv
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(u, c):
    await u.effective_message.reply_text("Hi")


def main():
    dotenv.load_dotenv()

    BOT_TOKEN = os.environ["BOT_API_KEY"]

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))

    app.run_polling()
