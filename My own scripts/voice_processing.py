
import openai 
from openai import OpenAI
import os
import sounddevice as sd
import soundfile as sf

client = OpenAI(
    api_key='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',
)


def audio_recorder(file_path, duration=4, sample_rate=44100):
    print(f"Recording audio for {duration} seconds. Speak into the microphone...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait for recording to complete
    sf.write(file_path, audio_data, sample_rate)
    print(f"Audio recording saved to {file_path}")


import speech_recognition as sr

def transcribe_audio_wav(wav_file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)

    # Perform the transcription
    try:
        transcription = recognizer.recognize_google(audio_data)
        return transcription
    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio"
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service"

# Replace 'recorded_audio.wav' with the path to your audio file
def voice_understand():
    audio_recorder():
    transcription = transcribe_audio_wav("recorded_audio.wav")
    return transcription 











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
    preprompt = "Your response will be used as raw code, so do not include any commentary. You are a desktop automation engine."
    llm_call(preprompt, prompt)
    return prompt

######################################################################