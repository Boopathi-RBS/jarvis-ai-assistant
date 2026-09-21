TASK_FILE = "tasks.txt"

def load_tasks():
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            return file.readlines()
    except:
        return []

def save_task(task):
    with open(TASK_FILE, "a", encoding="utf-8") as file:
        file.write(task + "\n")