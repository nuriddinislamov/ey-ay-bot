from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import dotenv
import logging
import openai

dotenv.load_dotenv()

BOT_TOKEN = os.environ["BOT_API_KEY"]
OPENAI_TOKEN = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(u, c):
    await u.effective_message.reply_text("Hi")


async def interact(u, c):
    text = u.effective_message.text

    try:
        c.user_data['no_of_reqs']
    except KeyError:
        c.user_data.update({'no_of_reqs': 0})

    c.user_data.update(
        {"no_of_reqs": c.user_data['no_of_reqs'] + 1}
    )

    if c.user_data['no_of_reqs'] <= 5:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{text}"}
            ]
        )

        reply = response['choices'][0]['message']['content']
    else:
        reply = "Sorry, the maximum times you can ask me is <b>5 times</b> for now. Don't worry, this will be updated soon!"

    await u.effective_message.reply_text(reply, parse_mode="HTML")


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))

    app.add_handler(MessageHandler(filters.TEXT, interact))

    app.run_polling()
