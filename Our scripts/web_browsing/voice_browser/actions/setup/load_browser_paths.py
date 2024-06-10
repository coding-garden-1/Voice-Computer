import json

def load_browser_paths():
    try:
        with open('jsons/browser_paths.json', 'r') as file:
            browser_paths = json.load(file)
        return browser_paths
    except FileNotFoundError:
        print('Error: browser_paths.json file not found.')
        return {}