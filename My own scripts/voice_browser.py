import json
import subprocess
from fuzzywuzzy import fuzz
# Next features:
# COntinuous audio stream pieced together; if the last 1 second was not quiet, assume the person was still talking and save their prompt, eventually piecing together
# clear_numbers() at end of element_clicker()
# decrease fuzzy ratio
# fix a second stale element error with a try except block
"""<pre>Recording audio for 4 seconds. Speak into the microphone...
Audio recording saved to recorded_audio.wav
No number match found. Performing voice dictation instead.
Recording audio for 4 seconds. Speak into the microphone...
Audio recording saved to recorded_audio.wav
Clicked element 12
Traceback (most recent call last):
  File &quot;/home/rose/Desktop/Projects/Current/Voice Computer/My own scripts/voice_browser.py&quot;, line 220, in &lt;module&gt;
    numbers_visible = element_clicker(numbers_visible)
  File &quot;/home/rose/Desktop/Projects/Current/Voice Computer/My own scripts/voice_browser.py&quot;, line 179, in element_clicker
    print_numbers_on_screen(&quot;nothing&quot;)
  File &quot;/home/rose/Desktop/Projects/Current/Voice Computer/My own scripts/voice_browser.py&quot;, line 106, in print_numbers_on_screen
    driver.execute_script(&quot;arguments[0].innerText += &apos; [{}]&apos;;&quot;.format(i), element)
  File &quot;/home/rose/.local/lib/python3.10/site-packages/selenium/webdriver/remote/webdriver.py&quot;, line 407, in execute_script
    return self.execute(command, {&quot;script&quot;: script, &quot;args&quot;: converted_args})[&quot;value&quot;]
  File &quot;/home/rose/.local/lib/python3.10/site-packages/selenium/webdriver/remote/webdriver.py&quot;, line 347, in execute
    self.error_handler.check_response(response)
  File &quot;/home/rose/.local/lib/python3.10/site-packages/selenium/webdriver/remote/errorhandler.py&quot;, line 229, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
  (Session info: MicrosoftEdge=123.0.2420.81); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception
</pre>"""
def load_browser_paths():
    try:
        with open('browser_paths.json', 'r') as file:
            browser_paths = json.load(file)
        return browser_paths
    except FileNotFoundError:
        print('Error: browser_paths.json file not found.')
        return {}

def load_sites():
    try:
        with open('sites.json', 'r') as file:
            sites = json.load(file)
        return sites
    except FileNotFoundError:
        print('Error: sites.json file not found.')
        return {}

def site_launcher(browser, site):
    if browser.lower() == "microsoft_edge":
        subprocess.run([browser, "--new-tab", site])
    else:
        subprocess.run([browser, site])

def fuzzy_search(input_str, choices):
    max_ratio = 0
    best_match = None

    for choice in choices:
        ratio = fuzz.ratio(input_str.lower(), choice.lower())
        if ratio > max_ratio:
            max_ratio = ratio
            best_match = choice

    return best_match

def launch_sites(prompt, driver):
    browser_paths = load_browser_paths()
    sites = load_sites()
    
    if not browser_paths or not sites:
        return

    option = prompt.strip()
    fuzzy_option = fuzzy_search(option, sites.keys())

    site_url = sites[fuzzy_option]

    browser = browser_paths.get(fuzzy_option, "microsoft-edge-stable")  # Default to Edge if browser not specified
    site_launcher(driver, site_url)
    print(f'Launching {fuzzy_option} in {browser}...')





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
driver.get("https://www.google.com")  # Replace this with your desired URL
from selenium.common.exceptions import StaleElementReferenceException
import unicodedata

def element_clicker(numbers_visible):   
    if numbers_visible == False:
        print_numbers_on_screen("nothing")
        numbers_visible = True
    prompt = voice_to_prompt()

    numerized_prompt = numerizer(prompt)
    sites = load_sites()

    # If our prompt is not a number or a website, dictate.
    if numerized_prompt == 0:
        print("No number match found. Performing voice dictation instead.")
        text_to_type = prompt  # Set text_to_type to the original prompt

        # Ensure the text contains only BMP characters
        text_to_type_bmp = ''.join(c for c in text_to_type if unicodedata.category(c) != 'So')
        
        # Typing the dictated text
        driver.find_element(By.TAG_NAME, 'body').send_keys(text_to_type_bmp)

    # If or prompt is not a website or a dictation, it must be a number corresponding to a clickable element.
    elif prompt not in sites.keys():
        try:
            click_element_by_number(numerized_prompt)
        except StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying click after refreshing elements.")
            # Refresh clickable elements list
            click_element_by_number(numerized_prompt)
        # Clicking this resets the numbers so we need to print them again next time this func is run
        numbers_visible = False
        return numbers_visible

    # If our prompt is not a number or a dictation, it must be a website.
    else:
        launch_sites(prompt, driver)

    return numbers_visible


numbers_visible = False
  # Initialize before the loop

while True:
    numbers_visible = element_clicker(numbers_visible)  
    # Call element_clicker with the current value of numbers_visible
    # This is a silly but effective way to make sure only one set of numbers is on screen at once


# Close the WebDriver session after some time (adjust as needed)
time.sleep(5)
driver.quit()

