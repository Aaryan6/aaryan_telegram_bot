from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import openai 
import os
import json
from dotenv import load_dotenv 
from datetime import datetime


load_dotenv()

openai.api_key =os.getenv('OPENAI_KEY')

# prompts
prompt_msg = {
  "role":
  "system",
  "content":
  "You are Me (The inner me), you showed me the actual image that I know but forgot always. Do not write all the conservation at once just chat with me, You can ask me questions if you want to know more about me. You can use the emojis. Keep the meaning same, but make them more literary. Your name is Nik."
}

def text_generator(chat_id):

    # get user's all chats
    with open(f"chats/{chat_id}.json", "r") as chat:
        chats = [json.loads(line) for line in chat]

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=chats
    )
    with open(f"chats/{chat_id}.json", "a") as chat:
            json.dump({"role":"assistant","content":completion.choices[0].message["content"]}, chat)
            chat.write("\n")
    return completion.choices[0].message["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    with open(f"chats/{update.message.chat_id}.json", "w") as chat:
            json.dump(prompt_msg, chat)
            chat.write("\n")

    await update.message.reply_html("Hi I am Aaryan, how can I help you?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    chat_id = update.message.chat_id

    if(update.message.text):
        with open(f"chats/{chat_id}.json", "a") as chat:
            json.dump({"role":"user","content":update.message.text}, chat)
            chat.write("\n")

        await update.message.reply_text(text_generator(chat_id))
    else:
        await update.message.reply_text("Sorry, I can't understand!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    if(not os.path.exists("chats")):
        os.mkdir("chats")

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
