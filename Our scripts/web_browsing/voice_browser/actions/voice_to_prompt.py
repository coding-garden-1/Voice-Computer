import sounddevice as sd
import soundfile as sf
from openai import OpenAI




def audio_recorder(file_path, duration=4, sample_rate=44100):
    print(f"Recording audio for {duration} seconds. Speak into the microphone...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait for recording to complete
    sf.write(file_path, audio_data, sample_rate)
    print(f"Audio recording saved to {file_path}")



def whisper_transcription(audio_file_path):
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

def llm_call(preprompt, transcript):
    with open("openai_key.txt","r") as file:
        key = file.read().strip()

    client = OpenAI(
        api_key=key,
    )
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
    try:
        audio_recorder("recorded_audio.wav")
        prompt = whisper_transcription("recorded_audio.wav")
        preprompt = "Your response will be used as raw code, so do not include any commentary. You are a desktop automation engine."
        llm_call(preprompt, prompt)
    except Exception as e:
        print("Error:" + str(e))
    return prompt