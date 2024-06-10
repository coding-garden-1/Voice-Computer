from setup.load_browser_paths import load_browser_paths
from setup.load_sites import load_sites 
from executing.site_launcher import site_launcher
from processing.fuzzy_search import fuzzy_search

def launch_sites(prompt, driver):
    browser_paths = load_browser_paths()
    sites = load_sites()
    
    if not browser_paths or not sites:
        return

    option = prompt.strip()
    fuzzy_option = fuzzy_search(option, sites.keys())

    site_url = sites[fuzzy_option]

    browser = browser_paths.get(fuzzy_option, "microsoft-edge-stable")  # Default to Edge if browser not specified
    site_launcher(driver, site_url)
    print(f'Launching {fuzzy_option} in {browser}...')
