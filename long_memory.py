MEMORY_FILE = "memory.txt"

def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as file:
        file.write(text + "\n")

def load_memories():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except:
        return ""