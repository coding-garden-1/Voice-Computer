from fuzzywuzzy import fuzz

def fuzzy_match(vocal_command, known_commands):
    fuzzy_known_commands = [command.lower() for command in known_commands.keys()]
    
    best_match_score = 0
    best_command = None

    for known_command in fuzzy_known_commands:
        match_score = fuzz.partial_ratio(vocal_command, known_command)
        if match_score > 80:  # Adjust the score threshold as needed
            if match_score > best_match_score:
                best_match_score = match_score
                best_command = known_command

    if best_command is not None:
        return known_commands.get(best_command)
    else:
        return None

