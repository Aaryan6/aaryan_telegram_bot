# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()
	
	
# Loop infinitely for user to
# speak

while(1):
	
	# Exception handling to handle
	# exceptions at the runtime
	try:
		
		# use the microphone as source for input.
		with sr.Microphone() as source2:
			
			# wait for a second to let the recognizer
			# adjust the energy threshold based on
			# the surrounding noise level
			r.adjust_for_ambient_noise(source2, duration=0.2)
			
			#listens for the user's input
			audio2 = r.listen(source2)
			
			# Using google to recognize audio
			MyText = r.recognize_google(audio2)
			MyText = MyText.lower()

			print("Did you say ",MyText)
			SpeakText(MyText)
			
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
		
	except sr.UnknownValueError:
		print("unknown error occurred")


# ---------------
 # file_info = await context.bot.get_file(update.update.message.voice.file_id)
    # unique_id = uuid.uuid4()
    # unique_filename = str(unique_id)
    # await file_info.download_to_drive(f"{unique_filename}.ogg")

    # ogg_filename = f"{unique_filename}.ogg"
    # wav_filename = "output_wav.wav"

    # convert_ogg_to_wav(ogg_filename, wav_filename)

    # await context.bot.send_message(chat_id=update.message.chat_id, text="recognized_text")