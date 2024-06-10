
from web_browsing.voice_browser import voice_browser
from command_processing.natural2command import natural2command
from command_processing.execute_command import execute_command
from command_processing.whisper import whisper
from command_processing.recorder import recorder 
from command_processing.known_commands import known_commands
from command_processing.fuzzy_match import fuzzy_match

known_commands = known_commands()

def main_loop():
    while True:
        recorded = recorder("recorded.wav")
        transcript = whisper(recorded)
        vocal_command = natural2command(transcript)
        best_match = fuzzy_match(vocal_command, known_commands)
        if best_match in known_commands:
            known_command = known_commands[best_match]
            execute_command(known_command)

main_loop()
