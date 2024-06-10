

import openai 
from openai import OpenAI


def whisper(audio_file_path):
    with open("openai_key.txt","r") as file:
        key = file.read().strip()

    client = OpenAI(
        api_key=key,
    )
    with open(audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,  # Pass the file object directly
            response_format="text"
        )
        return response