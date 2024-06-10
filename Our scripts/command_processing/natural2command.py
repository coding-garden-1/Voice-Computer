# natural_to_command.py


# Commands:


commands = """


open firefox 
click ___ (determine dynamically what 'search bar', 'text input bar', etc are, using Selenium and AI analysis of the webpage)

"""






system_content = f"""
you turn overall commands into specific instructions that different parts of a computer can understand. for example, 'computer, ask better GPT whats abstract algebra' would turn into 'go to better gpt', 'locate chat bar', 'type 'whats abstract algebra'', 'enter'. your response will be parsed as raw code, so just return the commands separated by commas.

the commands you can pull from are here:

{commands}

dont make up your own bc they wont be recognized by the python system.
"""



import openai 
from openai import OpenAI


def natural2command(transcript):
    with open("openai_key.txt","r") as file:
        key = file.read().strip()

    client = OpenAI(
        api_key=key,    
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system","content": system_content},
            {"role": "user", "content": transcript}
        ]
    )
    generated_message = completion.choices[0].message.content
    return generated_message

