from file_manager import list_files
from long_memory import load_memories
from tasks import load_tasks

def process_command(text):

    text = text.lower().strip()

    if "show memory" in text:
        return "MEMORY"

    elif "show tasks" in text:
        return "TASKS"

    elif "show files" in text:
        return "FILES"

    elif text.startswith("create "):
        return "CREATE_CODE"

    elif text.startswith("search "):
        return "SEARCH"

    elif text.startswith("read "):
        return "READ_FILE"

    elif text.startswith("improve "):
        return "IMPROVE_FILE"

    elif text.startswith("project note "):
        return "PROJECT_NOTE"

    elif "what are we building" in text:
        return "PROJECT_MEMORY"

    elif "take screenshot" in text:
        return "SCREENSHOT"

    elif any(
        phrase in text
        for phrase in [
            "open youtube",
            "youtube",
            "launch youtube",
            "start youtube"
        ]
    ):
        return "YOUTUBE"

    elif any(
        phrase in text
        for phrase in [
            "play songs",
            "play music",
            "music",
            "open music"
        ]
    ):
        return "MUSIC"

    elif any(
        phrase in text
        for phrase in [
            "spotify",
            "open spotify",
            "play spotify",
            "start spotify",
            "launch spotify"
        ]
    ):
        return "SPOTIFY"

    elif any(
        phrase in text
        for phrase in [
            "telegram",
            "open telegram",
            "start telegram",
            "launch telegram",
            "show telegram"
        ]
    ):
        return "TELEGRAM"

    elif any(
        phrase in text
        for phrase in [
            "shutdown",
            "turn off computer",
            "power off pc",
            "shutdown pc"
        ]
    ):
        return "SHUTDOWN"

    elif any(
        phrase in text
        for phrase in [
            "cancel shutdown",
            "stop shutdown",
            "abort shutdown",
            "don't shutdown",
            "do not shutdown"
        ]
    ):
        return "CANCEL_SHUTDOWN"

    elif text.startswith("open "):
        return "OPEN_APP"

    return "AI"