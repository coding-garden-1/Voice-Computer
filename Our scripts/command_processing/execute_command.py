# execute_command.py
# This just executes the command in a terminal. So the command probably needs to be formatted for the operating system, based on what we know about the software's CLI commands.
import subprocess

def execute_command(command):
	subprocess.run(command)