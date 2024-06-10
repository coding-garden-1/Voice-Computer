from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from .element_clicker import element_clicker


def launch_edge(url):

    # Initialize Edge WebDriver
    driver = webdriver.Edge()

    # Open a webpage
    driver.get(url)  # Replace this with your desired URL

    numbers_visible = False
  # Initialize before the loop

    while True:
        numbers_visible = element_clicker(numbers_visible)  
        # Call element_clicker with the current value of numbers_visible
        # This is a silly but effective way to make sure only one set of numbers is on screen at once

