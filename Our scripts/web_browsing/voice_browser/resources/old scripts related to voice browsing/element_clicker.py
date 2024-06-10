# Function to find clickable elements and click based on number
def click_element_by_number(driver, number):
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
def print_numbers_on_screen(driver, elements):
    try:
        # Clear existing number tags on the screen
        driver.execute_script("document.querySelectorAll('.number-tag').forEach(e => e.remove());")

        # Find clickable elements on the page
        clickable_elements = driver.find_elements(By.XPATH, "//button | //a | //input[@type='button']")
        
        # Print a new number next to each clickable element on the screen
        for i, element in enumerate(clickable_elements, 1):
            driver.execute_script("arguments[0].innerText += ' [{}]'".format(i), element)
            driver.execute_script("arguments[0].classList.add('number-tag')", element)  # Add a class to identify number tags
    except Exception as e:
        print(f"Error: {e}")




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