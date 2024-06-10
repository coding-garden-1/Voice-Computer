from fuzzywuzzy import fuzz
import json
import os

def fuzzy_search(input_str, choices):
    max_ratio = 0
    best_match = None

    for choice in choices:
        ratio = fuzz.ratio(input_str.lower(), choice.lower())
        if ratio > max_ratio:
            max_ratio = ratio
            best_match = choice

    return best_match

def make_browser_jsons(browser, executable_path, is_default):
    # Ensure browser_paths.json exists
    if not os.path.exists('browser_paths.json'):
        with open('browser_paths.json', 'w') as file:
            json.dump({}, file)

    with open('browser_paths.json', 'r') as file:
        browser_paths = json.load(file)

    # Check if a default browser is already set
    default_browser = None
    for browser_name, browser_info in browser_paths.items():
        if isinstance(browser_info, dict) and browser_info.get('default'):
            default_browser = browser_name
            break

    if default_browser and is_default:
        # Reset all browsers to non-default
        for browser_name, browser_info in browser_paths.items():
            if isinstance(browser_info, dict):
                browser_info['default'] = False

    # Update or create the new browser entry
    browser_paths[browser] = {'executable_path': executable_path, 'default': is_default}

    with open('browser_paths.json', 'w') as file:
        json.dump(browser_paths, file, indent=4)

    # Update default_browser.txt if setting a new default
    if is_default:
        with open('default_browser.txt', 'w') as file:
            file.write(executable_path)

def make_site_jsons(site, address, browser=None):
    # Ensure sites.json exists
    if not os.path.exists('sites.json'):
        with open('sites.json', 'w') as file:
            json.dump({}, file)

    with open('sites.json', 'r') as file:
        sites_data = json.load(file)

    if browser is None:
        # Check if there's a default browser set
        with open('browser_paths.json', 'r') as file:
            browser_paths = json.load(file)
        for browser_name, browser_info in browser_paths.items():
            if isinstance(browser_info, dict) and browser_info.get('default'):
                browser = 'default'
                break

    sites_data[site] = {'address': address, 'browser': browser}

    with open('sites.json', 'w') as file:
        json.dump(sites_data, file, indent=4)

# Uncomment the line below to generate the JSON files initially
while input("Add more browsers? (y/n): ") in ["y", "yes"]:
    browser_input = input("Browser name: ")
    browser_executable = input("Browser executable path: ")
    while not browser_executable:  # Prompt until a valid path is provided
        print("Browser executable path cannot be empty.")
        browser_executable = input("Browser executable path: ")
    is_default_input = input("Is this the default browser? (Type 'y' for yes, otherwise just hit enter): ")

    is_default = is_default_input.lower() == 'y'
    make_browser_jsons(browser_input, browser_executable, is_default)

# Ensure browser_paths.json exists
if not os.path.exists('browser_paths.json'):
    with open('browser_paths.json', 'w') as file:
        json.dump({}, file)

default_browser = None
with open('browser_paths.json', 'r') as file:
    browser_paths = json.load(file)
    for browser_name, browser_info in browser_paths.items():
        if isinstance(browser_info, dict) and browser_info.get('default'):
            default_browser = browser_name
            break

while input("Add more sites? (y/n): ") in ["y", "yes"]:
    site = input("Site name: ")
    site_address = input("Site URL: ")
    specific_browser_or_no = input("Any specific browser? (YES/NO): ")
    if specific_browser_or_no.lower() in ['yes', 'y']:
        specific_browser = input('Browser name: ')
        best_match = fuzzy_search(specific_browser, browser_paths.keys())
        specific_browser = best_match if best_match else None
    else:
        specific_browser = default_browser

    make_site_jsons(site, site_address, specific_browser)
