from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# Define a few command handlers. These usually take the two arguments update and
# context.

# open ai gpt
openai.api_key =os.getenv('OPENAI_KEY')

# prompts
mess=[{"role": "system", "content": "Behave like a 19 year-old boy named Aaryan Patel, Aaryan is a very smart boy and passionate about programming, his profession is full stack development. give answer in short. give answer in a playful and mischievous manner"},{"role":"user","content":"Hi"}]


def text_generator():
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[msg for msg in mess]
    )
    mess.append({"role":completion.choices[0].message["role"],"content":completion.choices[0].message["content"]})
    return completion.choices[0].message["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html("Hi I am Aaryan, how can I help you?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    mess.append({
    "content": update.message.text,
    "role": "user"
    })

    if(update.message.text):
        await update.message.reply_text(text_generator())
    else:
        await update.message.reply_text("Sorry, I can't understand!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TELEGRAM_KEY')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()