import subprocess

def site_launcher(browser, site):
    if browser.lower() == "microsoft_edge":
        subprocess.run([browser, "--new-tab", site])
    else:
        subprocess.run([browser, site])


# It's strange that this function is calling a subprocess command.
# The motherboards of the voice computer are supposed to merely
# determine the command to be executed by execute_command,
# NOT execute anything themselves.