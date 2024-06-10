
import json

def make_browser_jsons(browser, executable_path):
    try:
        with open('browser_paths.json', 'r') as file:
            browser_paths = json.load(file)
    except FileNotFoundError:
        browser_paths = {}

    browser_paths[browser] = executable_path

    with open('browser_paths.json', 'w') as file:
        json.dump(browser_paths, file, indent=4)

def make_site_jsons(site, address):
    try:
        with open('sites.json', 'r') as file:
            sites_data = json.load(file)
    except FileNotFoundError:
        sites_data = {}

    sites_data[site] = address

    with open('sites.json', 'w') as file:
        json.dump(sites_data, file, indent=4)


# Uncomment the line below to generate the JSON files initially
while input("Add more browsers? (y/n): ") in ["y", "yes"]:
    browser = input("Browser name: ")
    browser_executable = input("Browser executable path: ")
    make_browser_jsons(browser,browser_executable)
while input("Add more sites? (y/n): ") in ["y", "yes"]:
    site = input("Site name: ")
    site_address = input("Site URL: ")
    make_site_jsons(site,site_address)

