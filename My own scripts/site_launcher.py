import json
import subprocess
from fuzzywuzzy import fuzz

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

def launch_sites():
    browser_paths = load_browser_paths()
    sites = load_sites()
    
    if not browser_paths or not sites:
        return
    
    print('Available options:')
    for key in sites.keys():
        print(f'- {key}')

    option = input('Enter the option you would like to launch: ').strip()
    fuzzy_option = fuzzy_search(option, sites.keys())
    
    if not fuzzy_option:
        print('Invalid option.')
        return

    site_url = sites[fuzzy_option]

    browser = browser_paths.get(fuzzy_option, "microsoft-edge-stable")  # Default to Edge if browser not specified
    site_launcher(browser, site_url)
    print(f'Launching {fuzzy_option} in {browser}...')

launch_sites()
