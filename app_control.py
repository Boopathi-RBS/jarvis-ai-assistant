import os

def open_app(command):

    command = command.lower()

    if "notepad" in command:
        os.system("start notepad")
        return "Opening Notepad..."

    elif "calculator" in command:
        os.system("start calc")
        return "Opening Calculator..."

    elif "paint" in command:
        os.system("start mspaint")
        return "Opening Paint..."

    elif "chrome" in command:
        os.system("start chrome")
        return "Opening Chrome..."

    return None