import json

def load_sites():
    try:
        with open('jsons/sites.json', 'r') as file:
            sites = json.load(file)
        return sites
    except FileNotFoundError:
        print('Error: sites.json file not found.')
        return {}