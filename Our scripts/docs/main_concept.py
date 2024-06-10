# main.py 

from voice_processing import voice_understanding
from browsing_setup import make_browser_jsons
from browsing_setup import make_site_jsons
from site_launcher import launch_sites
from execute_command import execute_command

def main_loop():
	while True:
		vocal_command = voice_understand()
		if vocal_command in any fuzzy command in known commands:
			execute_command(the corresponding command)


if input('Already setup? (y/n): ') == 'y':
	main_loop()
