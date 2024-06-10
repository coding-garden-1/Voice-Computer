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