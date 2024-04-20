
import openai 
from openai import OpenAI
import os
import sounddevice as sd
import soundfile as sf
import pyautogui 

with open("openai_key.txt", "r") as file:
	key = file.read()

client = OpenAI(
    api_key=key
)

def audio_recorder(file_path, duration=4, sample_rate=44100):
    print(f"Recording audio for {duration} seconds. Speak into the microphone...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait for recording to complete
    sf.write(file_path, audio_data, sample_rate)
    print(f"Audio recording saved to {file_path}")


###################AI Version##########################

#######################################################
def whisper_transcription(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,  # Pass the file object directly
            response_format="text"
        )
        return response

def llm_call(preprompt, transcript):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": preprompt},
            {"role": "user", "content": transcript}
        ]
    )
    generated_message = completion.choices[0].message.content
    return generated_message


def voice_to_prompt():
    audio_recorder("recorded_audio.wav")
    prompt = whisper_transcription("recorded_audio.wav")
    preprompt = "Your response will be used as raw code, so do not include any commentary. You return the code the user wants directly, such that your raw responss would throw without error."
    code = ""
    if "Alexa" in prompt.split(): 
    	code = llm_call(preprompt, prompt)
    print(code)
    return code
    

def typer():
	while True:
		code = voice_to_prompt()
		pyautogui.write(code)
######################################################################