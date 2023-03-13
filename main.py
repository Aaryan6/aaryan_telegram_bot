from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import openai 
import os
import schedule
from dotenv import load_dotenv 
from datetime import datetime


load_dotenv()

openai.api_key =os.getenv('OPENAI_KEY')

# prompts
prompt_msg = {
  "role":
  "system",
  "content":
  "Behave like a 19 year-old boy named Aaryan Patel, Aaryan is a very smart boy and passionate about programming, his profession is full stack development. give answer in short. give answer in a playful and mischievous manner"
}

message_history={}
response_time={}

def text_generator(chat_id):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[msg for msg in message_history[chat_id]]
    )
    message_history[chat_id].append({"role":completion.choices[0].message["role"],"content":completion.choices[0].message["content"]})
    return completion.choices[0].message["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_html("Hi I am Aaryan, how can I help you?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    chat_id = update.message.chat_id
    now = datetime.now()
    
    if(response_time.get(chat_id)):
        difference=now-response_time.get(chat_id)
        if(difference.total_seconds()>3600):
            message_history[chat_id]=[prompt_msg]
    response_time[chat_id] = now

    if(not message_history.get(chat_id)):
        message_history[chat_id]=[prompt_msg]

    if(update.message.text):
        message_history[chat_id].append({
        "content": update.message.text,
        "role": "user"
        })
        await update.message.reply_text(text_generator(chat_id))
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
