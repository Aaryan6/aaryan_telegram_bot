from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import openai

# Define a few command handlers. These usually take the two arguments update and
# context.

# open ai gpt
openai.api_key ='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'

def aiBot(txt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Behave as a 19 years old boy that name is Aaryan and give answers as an expert in every field: {txt}?",
    temperature=0.7,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=["Aaryan:","User:"]
    )
    return response.choices[0].text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html("Hi I am Aaryan, how can I help you?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if(update.message.text):
        await update.message.reply_text(aiBot(update.message.text))
    else:
        await update.message.reply_text("Sorry, I can't understand!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('6242418841:AAHogKrTkS07Yq1VZRJZg13ECmv09CYhkOo').build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
