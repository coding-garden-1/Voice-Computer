
import openai 
from openai import OpenAI
import os
import sounddevice as sd
import soundfile as sf
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from fuzzywuzzy import fuzz

client = OpenAI(
    api_key='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',
)


def audio_recorder(file_path, duration=4, sample_rate=44100):
    print(f"Recording audio for {duration} seconds. Speak into the microphone...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait for recording to complete
    sf.write(file_path, audio_data, sample_rate)
    print(f"Audio recording saved to {file_path}")

# Function to find clickable elements and click based on number
def click_element_by_number(number):
    try:
        # Find all clickable elements on the page
        clickable_elements = driver.find_elements(By.XPATH, "//button | //a | //input[@type='button']")
        # Print a little number next to each one on the screen
        print_numbers_on_screen(clickable_elements)
        # If the given number is valid, click the corresponding element
        if 0 < number <= len(clickable_elements):
            clickable_elements[number - 1].click()
            print(f"Clicked element {number}")
        else:
            print("Invalid number. Please provide a valid number.")
    except Exception as e:
        print(f"Error: {e}")

# Function to print numbers next to clickable elements on the screen
def print_numbers_on_screen(elements):
    clickable_elements = driver.find_elements(By.XPATH, "//button | //a | //input[@type='button']")
        # Print a little number next to each one on the screen
    for i, element in enumerate(clickable_elements, 1):
        driver.execute_script("arguments[0].innerText += ' [{}]';".format(i), element)
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
    try:
        audio_recorder("recorded_audio.wav")
        prompt = whisper_transcription("recorded_audio.wav")
        preprompt = "Your response will be used as raw code, so do not include any commentary. You are a desktop automation engine."
        llm_call(preprompt, prompt)
    except Exception as e:
        print("Error:" + str(e))
    return prompt

from fuzzywuzzy import process, fuzz

def numerizer(prompt):
    # Define a dictionary mapping numbers to their textual representations
    number_mapping = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
        'twenty-one': 21, 'twenty-two': 22, 'twenty-three': 23, 'twenty-four': 24, 'twenty-five': 25,
        'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28, 'twenty-nine': 29, 'thirty': 30,
        'thirty-one': 31, 'thirty-two': 32, 'thirty-three': 33, 'thirty-four': 34, 'thirty-five': 35,
        'thirty-six': 36, 'thirty-seven': 37, 'thirty-eight': 38, 'thirty-nine': 39, 'forty': 40,
        'forty-one': 41, 'forty-two': 42, 'forty-three': 43, 'forty-four': 44, 'forty-five': 45,
        'forty-six': 46, 'forty-seven': 47, 'forty-eight': 48, 'forty-nine': 49, 'fifty': 50,
    }

    # Check if the prompt is a textual representation of a number
    closest_match = process.extractOne(prompt, number_mapping.keys(), scorer=fuzz.partial_ratio)
    if closest_match[1] > 80:
        return number_mapping[closest_match[0]]

    # Check if the prompt is a direct match to a number
    if prompt in number_mapping:
        return number_mapping[prompt]

    # Return 0 if no match is found
    return 0


# Initialize Edge WebDriver
driver = webdriver.Edge()

# Open a webpage
driver.get("https://example.com")  # Replace this with your desired URL
def element_clicker():   
    print_numbers_on_screen("nothing")
    prompt = voice_to_prompt()

    numerized_prompt = numerizer(prompt)
    click_element_by_number(numerized_prompt)

while True:
    element_clicker() 
    
# Close the WebDriver session after some time (adjust as needed)
time.sleep(5)
driver.quit()
