from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Updater
import openai 
import os
from os import path
import json
from dotenv import load_dotenv 
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment
import soundfile as sf
import uuid
import logging
import io
import urllib

# Set up logging (optional but helpful for debugging)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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

# start function for bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    with open(f"chats/{update.message.chat_id}.json", "w") as chat:
            json.dump(prompt_msg, chat)
            chat.write("\n")

    await update.message.reply_html("Hi I am Aaryan, how can I help you?")

# help command for bot
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

# sending message to user
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    chat_id = update.message.chat_id

    if(update.message.text):
        with open(f"chats/{chat_id}.json", "a") as chat:
            json.dump({"role":"user","content":update.message.text}, chat)
            chat.write("\n")

        # await update.message.reply_text(text_generator(chat_id))
        await update.message.reply_text("Hey! I am a bot")
    else:
        await update.message.reply_text("Sorry, I can't understand!")

# convert ogg to wav
def ogg2wav(ogg_url):

    ogg_audio = AudioSegment.from_ogg(io.BytesIO(urllib.request.urlopen(ogg_url).read()))
    wav_audio = io.BytesIO()
    ogg_audio.export(wav_audio, format='wav')
    return wav_audio.getvalue()


# voice to voice conversion
async def dhwani(update: Update, context) -> None:
    message = update.message
    bot = context.bot
    file_id = update.message.voice.file_id

    # Get the file object from Telegram's servers
    file = await bot.get_file(file_id)

    # ogg_url = file.file_path
    voice_file = file.file_path
    wav_data = ogg2wav(voice_file)
    recognizer = sr.Recognizer()
    try:
        # Recognize the speech from the voice file
        with sr.AudioFile(io.BytesIO(wav_data)) as source:
            audio_data = recognizer.record(source)

        # Send the recognized text back to the user
        audio_text = recognizer.recognize_google(audio_data)

        # Send the recognized text back to the user
        await message.reply_text(audio_text)
    except sr.UnknownValueError:
        await message.reply_text("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        await message.reply_text("Sorry, there was an error processing the audio. Please try again later.")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    if(not os.path.exists("chats")):
        os.mkdir("chats")
    if(not os.path.exists("voices")):
        os.mkdir("voices")
    if(not os.path.exists("wav_file")):
        os.mkdir("wav_file")

    application = Application.builder().token('6242418841:AAHogKrTkS07Yq1VZRJZg13ECmv09CYhkOo').build()
    # application = Application.builder().token(os.getenv('TELEGRAM_KEY')).build()

    # start command
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # text message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # voice message
    application.add_handler(MessageHandler(filters.VOICE, dhwani))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
