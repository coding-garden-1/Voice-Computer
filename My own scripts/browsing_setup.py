import json
from fuzzywuzzy import fuzz

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
    try:
        with open('browser_paths.json', 'r') as file:
            browser_paths = json.load(file)
    except FileNotFoundError:
        browser_paths = {}

    if is_default:
        # Remove existing default flag if any
        for _, info in browser_paths.items():
            info['default'] = False

    browser_paths[browser] = {'executable_path': executable_path, 'default': is_default}

    with open('browser_paths.json', 'w') as file:
        json.dump(browser_paths, file, indent=4)

def make_site_jsons(site, address, browser=None):
    try:
        with open('sites.json', 'r') as file:
            sites_data = json.load(file)
    except FileNotFoundError:
        sites_data = {}

    if browser is None:
        # Check if there's a default browser set
        with open('browser_paths.json', 'r') as file:
            browser_paths = json.load(file)
        for browser_name, browser_info in browser_paths.items():
            if browser_info.get('default'):
                browser = browser_name
                break

    sites_data[site] = {'address': address, 'browser': browser}

    with open('sites.json', 'w') as file:
        json.dump(sites_data, file, indent=4)

# Uncomment the line below to generate the JSON files initially
while input("Add more browsers? (y/n): ") in ["y", "yes"]:
    browser_input = input("Browser name: ")
    browser_executable = input("Browser executable path: ")
    is_default_input = input("Is this the default browser? (Type 'y' for yes, otherwise just hit enter): ")

    is_default = is_default_input.lower() == 'y'
    make_browser_jsons(browser_input, browser_executable, is_default)

default_browser = None
with open('browser_paths.json', 'r') as file:
    browser_paths = json.load(file)
    for browser_name, browser_info in browser_paths.items():
        if browser_info.get('default'):
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
