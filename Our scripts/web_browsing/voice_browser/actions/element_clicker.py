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