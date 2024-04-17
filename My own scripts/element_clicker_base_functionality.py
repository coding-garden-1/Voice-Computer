from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize Edge WebDriver
driver = webdriver.Edge()

# Open a webpage
driver.get("https://example.com")  # Replace this with your desired URL

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
    for i, element in enumerate(elements, 1):
        driver.execute_script("arguments[0].innerText += ' [{}]';".format(i), element)

# Example usage: Click element number 3
click_element_by_number(1)

# Close the WebDriver session after some time (adjust as needed)
time.sleep(5)
driver.quit()
