import os
import shutil

def backup_file(filename):

    backup_name = filename + ".backup"

    shutil.copy(
        filename,
        backup_name
    )

    return backup_name
def list_files(folder="."):
    return os.listdir(folder)

def read_file(filename):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        return str(e)
    
def write_file(filename, content):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)
        
def append_file(filename, content):

    with open(
        filename,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(content)
def read_project_memory():

    try:

        with open(
            "project_memory.txt",
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except:

        return "No project memory found."
    
def append_project_memory(text):

    with open(
        "project_memory.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n" + text)