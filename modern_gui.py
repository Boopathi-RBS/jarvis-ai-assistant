import os
import time
import subprocess
import logging
import customtkinter as ctk
import webbrowser
from ai_brain import ask_ai, add_assistant_message
from voice_input import listen
from voice_output import speak, stop_speaking
from tray_icon import run_tray
from code_generator import save_python_file
from file_manager import (
    list_files,
    read_file,
    write_file,
    append_file,
    backup_file,
    read_project_memory,
    append_project_memory
)
from command_processor import process_command
from app_control import open_app
from web_search import search_web
from screenshot import take_screenshot
from system_commands import process_system_command
from permissions import (
    show_permissions,
    set_permission,
    load_permissions
)
from threading import Thread, Lock
from queue import Queue

conversation_running = False
conversation_lock = Lock()
ai_lock = Lock()

voice_queue = Queue()
last_voice_command = ""
last_command_time = 0

from wake_word import (
    wake_listener,
    pause_wake_listener,
    resume_wake_listener
)

logging.basicConfig(
    filename="boopathi.log",
    level=logging.ERROR
)

from long_memory import (
    load_memories,
    save_memory
)

from tasks import (
    load_tasks,
    save_task
)

ctk.set_appearance_mode("dark")

window = ctk.CTk()
window.title("Boopathi AI")

Thread(
    target=wake_listener,
    args=(window,),
    daemon=True
).start()

run_tray(window)

window.geometry("900x700")
window.withdraw()
# -------------------------
# FUNCTIONS
# -------------------------

def clear_chat():
    chat_box.delete("1.0", "end")


def show_memory():

    memories = load_memories()

    if not memories or memories.strip() == "":
        memories = "No memories saved."

    chat_box.insert(
        "end",
        f"\n🧠 Memories:\n{memories}\n\n"
    )

    chat_box.see("end")


def show_tasks():

    tasks = load_tasks()

    if not tasks:
        chat_box.insert(
            "end",
            "\n📋 No tasks found.\n\n"
        )

        chat_box.see("end")
        return

    chat_box.insert(
        "end",
        "\n📋 Tasks:\n"
    )

    for i, task in enumerate(tasks, start=1):
        chat_box.insert(
            "end",
            f"{i}. {task.strip()}\n"
        )

    chat_box.insert("end", "\n")
    chat_box.see("end")


def add_task():

    task = entry.get().strip()

    if not task:
        return

    save_task(task)

    chat_box.insert(
        "end",
        f"\n✅ Task Added: {task}\n\n"
    )

    chat_box.see("end")

    entry.delete(0, "end")

def generate_code():

    topic = entry.get()

    if topic.strip() == "":
        return

    prompt = f"""
Write only valid Python code.

Do not use markdown.
Do not use triple backticks.
Do not explain anything.

Create a Python program for:
{topic}
"""

    code = ask_ai(prompt)

    filename = topic.replace(" ", "_") + ".py"

    save_python_file(filename, code)

    chat_box.insert(
        "end",
        f"\n💻 Created: {filename}\n\n"
    )

    entry.delete(0, "end")

def create_code_with_ai(request):

    prompt = f"""
Write only valid Python code.

Do not use markdown.
Do not use triple backticks.
Do not explain anything.

Create:
{request}
"""

    code = ask_ai(prompt)

    filename = (
        request
        .replace("create ", "")
        .replace(" ", "_")
        + ".py"
    )

    save_python_file(
        filename,
        code
    )

    return filename

def improve_file(filename):

    backup_name = backup_file(filename)

    content = read_file(filename)

    prompt = f"""
Improve this Python code.

Return ONLY the improved code.

{content}
"""

    improved_code = ask_ai(prompt)

    write_file(
        filename,
        improved_code
    )

    return backup_name

def run_code():

    filename = entry.get().strip()

    if filename == "":
        return

    if not filename.endswith(".py"):
        filename += ".py"

    if os.path.exists(filename):

        chat_box.insert(
            "end",
            f"\n▶ Running {filename}\n\n"
        )

        subprocess.run(
            ["python", filename]
        )

    else:

        chat_box.insert(
            "end",
            f"\n❌ File not found: {filename}\n\n"
        )

def show_files():

    files = list_files()

    chat_box.insert(
        "end",
        "\n📂 Files:\n"
    )

    for file in files:

        chat_box.insert(
            "end",
            f"{file}\n"
        )

    chat_box.insert(
        "end",
        "\n"
    )

def open_file():

    filename = entry.get().strip()

    if filename == "":
        return

    content = read_file(filename)

    chat_box.insert(
        "end",
        f"\n📄 {filename}\n\n{content}\n\n"
    )

def save_text_to_file():

    filename = entry.get().strip()

    if filename == "":
        return

    content = chat_box.get( "1.0", "end" )

    print("Saving to:", os.path.abspath(filename))
    write_file(filename, content)

    chat_box.insert(
        "end",
        f"\n💾 Saved to {filename}\n\n"
    )

def capture_screen():

    filename = take_screenshot()

    chat_box.insert(
        "end",
        f"\n📸 Screenshot saved:\n{filename}\n\n"
    )

    chat_box.see("end")

def reply(answer):

    add_assistant_message(answer)

    return answer

def process_user_message(user_message):

    lower_msg = user_message.lower()

    # -----------------------
    # Show Permissions
    # -----------------------
    if lower_msg == "show permissions":

        return show_permissions()

    # -----------------------
    # Enable Permission
    # -----------------------
    if lower_msg.startswith("enable "):

        permission = lower_msg.replace(
            "enable ",
            ""
        ).strip()

        permissions = load_permissions()

        if permission not in permissions:
            return f"I don't know the permission '{permission}'."

        set_permission(
            permission,
            True
        )

        return f"{permission} permission enabled."

    # -----------------------
    # Disable Permission
    # -----------------------
    if lower_msg.startswith("disable "):

        permission = lower_msg.replace(
            "disable ",
            ""
        ).strip()

        permissions = load_permissions()

        if permission not in permissions:
            return f"I don't know the permission '{permission}'."

        set_permission(
            permission,
            False
        )

        return f"{permission} permission disabled."
    
    system_answer = process_system_command(user_message)

    if system_answer:
        return system_answer

    # -----------------------
    # Memory
    # -----------------------
    if lower_msg.startswith("remember "):

        memory = user_message[9:].strip()

        save_memory(memory)

        return f"Saved memory: {memory}"
    elif lower_msg == "what do you remember":

        return load_memories()

    command = process_command(user_message)

    print(f"[DEBUG] COMMAND = {command}")

    if command == "MEMORY":

        return load_memories()

    elif command == "TASKS":

        tasks = load_tasks()

        return "\n".join(
            [task.strip() for task in tasks]
        )
    
    elif lower_msg.startswith("add task "):

        task = user_message[9:].strip()

        save_task(task)

        return f"Task added: {task}"

    elif command == "FILES":

        files = list_files()

        return "\n".join(files)

    elif command == "OPEN_APP":

        return open_app(user_message)

    elif command == "SEARCH":

        return search_web(user_message)

    elif command == "READ_FILE":

        filename = (
            user_message
            .replace("read ", "")
            .strip()
        )

        return read_file(filename)

    elif command == "SCREENSHOT":

        filename = take_screenshot()

        return f"Screenshot saved as {filename}"

    elif command == "CREATE_CODE":

        filename = create_code_with_ai(
            user_message
        )

        return f"Created {filename}"

    elif command == "IMPROVE_FILE":

        filename = (
            user_message
            .replace("improve ", "")
            .strip()
        )

        backup_name = improve_file(filename)

        return (
            f"Improved {filename}\n"
            f"Backup created: {backup_name}"
        )

    elif command == "PROJECT_MEMORY":

        return read_project_memory()

    elif command == "PROJECT_NOTE":

        note = (
            user_message
            .replace("project note ", "")
            .strip()
        )

        append_project_memory(note)

        return "Project memory updated."
    
    elif command == "YOUTUBE":

        webbrowser.open("https://www.youtube.com")

        return reply("Opening Youtube")
    
    elif command == "MUSIC":

        os.startfile(
            r"C:\Users\BOOPATHI R\Music\Songs"
        )

        return reply("Opening Music Folder")
    
    elif command == "SPOTIFY":

        os.startfile("spotify")

        return reply("Opening Spotify")
    
    elif command == "TELEGRAM":

        os.startfile(
            r"C:\Users\BOOPATHI\AppData\Roaming\Telegram Desktop\Telegram.exe"
        )

        return reply("Opening Telegram")
    
    elif command == "SHUTDOWN":

        os.system(
            "shutdown /s /t 10"
        )

        return (
            "Shutting down computer "
            "in 10 seconds"
        )
    
    elif command == "CANCEL_SHUTDOWN":

        os.system(
            "shutdown /a"
        )

        return "Shutdown cancelled"

    else:

        return ask_ai(user_message)
    
def ai_worker():

    while True:

        user_message = voice_queue.get()

        if user_message is None:
            break

        window.after(
            0,
            lambda msg=user_message: (
                chat_box.insert(
                    "end",
                    f"You 🎤: {msg}\n\n"
                ),
                chat_box.see("end")
            )
        )

        window.after(
            0,
            lambda: status_label.configure(
                text="Thinking..."
            )
        )

        with ai_lock:

            answer = process_user_message(user_message)

        window.after(
            0,
            lambda: status_label.configure(
                text="Speaking..."
            )
        )

        window.after(
            0,
            lambda ans=answer: (
                chat_box.insert(
                    "end",
                    f"AI 🤖: {ans}\n\n"
                ),
                chat_box.see("end")
            )
        )

        speak(answer)

        window.after(
            0,
            lambda: status_label.configure(
                text="Listening..."
            )
        )

        voice_queue.task_done()
    
def process_message_thread(user_message):

    answer = process_user_message(user_message)
    voice_queue.put(user_message)

    window.after(
        0,
        lambda: finish_response(answer)
    )

def finish_response(answer):

    print("FINISH RESPONSE CALLED")

    # Speaking state
    status_label.configure(
        text="Speaking..."
    )

    print("SPEAKING:", answer)

    speak(answer)

    chat_box.insert(
        "end",
        f"AI 🤖: {answer}\n\n"
    )

    chat_box.see("end")

    # Back to ready
    status_label.configure(
        text="Ready"
    )

    resume_wake_listener()
    
def send_message():

    user_message = entry.get().strip()

    if not user_message:
        return

    chat_box.insert(
        "end",
        f"You: {user_message}\n\n"
    )
    # AI response

    status_label.configure(
        text="Thinking..."
    )

    Thread(
        target=process_message_thread,
        args=(user_message,),
        daemon=True
    ).start()

    entry.delete(0, "end")

def process_voice_thread(user_message):

    print("VOICE THREAD STARTED")

    answer = process_user_message(
        user_message
    )

    print("AI ANSWER:", answer)

    window.after(
        0,
        lambda: finish_response(answer)
    )

def conversation_mode():

    global conversation_running

    with conversation_lock:

        if conversation_running:
            print("Conversation already running.")
            return

        conversation_running = True

        silence_count = 0
        MAX_SILENCE = 4
        

    while True:

        window.after(
            0,
            lambda: status_label.configure(
                text="Listening..."
            )
        )

        user_message = listen()

        global last_voice_command
        global last_command_time

        current_time = time.time()

        cleaned_message = user_message.strip().lower() if user_message else ""

        if (
            cleaned_message
            and cleaned_message == last_voice_command
            and current_time - last_command_time < 2
        ):
            print("Duplicate command ignored.")
            continue

        if user_message:

            cleaned_message = user_message.strip().lower()

            if len(cleaned_message) > 3:

                last_voice_command = cleaned_message
                last_command_time = current_time

        if not user_message:

            silence_count += 1

            print(f"Silent attempts: {silence_count}")

            if silence_count >= MAX_SILENCE:

                speak("Going back to sleep.")

                window.after(
                    0,
                    lambda: status_label.configure(
                        text="Ready"
                    )
                )

                resume_wake_listener()

                conversation_running = False

                break

            continue
       
        silence_count = 0

        window.after(
            0,
            lambda: status_label.configure(
                text="Thinking..."
            )
        )

        if user_message.lower() in [
            "stop talking",
            "be quiet",
            "enough",
            "wait",
            "that's enough",
            "silent"
        ]:

            stop_speaking()

            continue

        voice_queue.put(user_message)

        if user_message.lower() in [
            "stop",
            "stop listening",
            "exit",
            "goodbye",
            "bye jarvis"
        ]:

            speak("Goodbye.")

            window.after(
                0,
                lambda: status_label.configure(
                    text="Ready"
                )
            )

            resume_wake_listener()

            conversation_running = False

            break

def voice_message():

    print("VOICE MESSAGE STARTED")

    pause_wake_listener()

    try:

        user_message = listen()

        print("VOICE HEARD:", user_message)

        if not user_message:

            print("NO VOICE DETECTED")

            resume_wake_listener()

            status_label.configure(text="Ready")

            return
        
        Thread(
            target=process_voice_thread,
            args=(user_message,),
            daemon=True
        ).start()

    except Exception as e:

        print("VOICE ERROR:", e)

        resume_wake_listener()

        logging.exception(e)


# -------------------------
# SIDEBAR
# -------------------------

sidebar = ctk.CTkFrame(window, width=200)
sidebar.pack(side="left", fill="y")

sidebar_title = ctk.CTkLabel(
    sidebar,
    text="Boopathi AI",
    font=("Arial", 22)
)

sidebar_title.pack(pady=20)

notes_button = ctk.CTkButton(
    sidebar,
    text="📄 Notes"
)

notes_button.pack(pady=10, padx=10)

clear_button = ctk.CTkButton(
    sidebar,
    text="🗑 Clear Chat",
    command=clear_chat
)

clear_button.pack(pady=10, padx=10)

memory_button = ctk.CTkButton(
    sidebar,
    text="🧠 View Memory",
    command=show_memory
)

memory_button.pack(pady=10, padx=10)

task_button = ctk.CTkButton(
    sidebar,
    text="📋 show Tasks",
    command=show_tasks
)

task_button.pack(pady=10, padx=10)

add_task_button = ctk.CTkButton(
    sidebar,
    text="➕ Add Task",
    command=add_task
)

add_task_button.pack(pady=10, padx=10)

generate_button = ctk.CTkButton(
    sidebar,
    text="💻 Generate Code",
    command=generate_code
)

generate_button.pack(pady=10, padx=10)

run_button = ctk.CTkButton(
    sidebar,
    text="▶ Run Code",
    command=run_code
)

run_button.pack(pady=10, padx=10)

files_button = ctk.CTkButton(
    sidebar,
    text="📂 Show Files",
    command=show_files
)

files_button.pack(pady=10, padx=10)

open_file_button = ctk.CTkButton(
    sidebar,
    text="📄 Open File",
    command=open_file
)

open_file_button.pack(pady=10, padx=10)

save_file_button = ctk.CTkButton(
    sidebar,
    text="💾 Save File",
    command=save_text_to_file
)

save_file_button.pack(
    pady=10,
    padx=10
)

screenshot_button = ctk.CTkButton(
    sidebar,
    text="📸 Screenshot",
    command=capture_screen
)

screenshot_button.pack(
    pady=10,
    padx=10
)

# -------------------------
# MAIN AREA
# -------------------------

main_frame = ctk.CTkFrame(window)
main_frame.pack(
    side="right",
    fill="both",
    expand=True
)

status_label = ctk.CTkLabel(
    main_frame,
    text="Ready"
)

status_label.pack(pady=5)

title = ctk.CTkLabel(
    main_frame,
    text="Boopathi AI Assistant",
    font=("Arial", 24)
)

title.pack(pady=20)

chat_box = ctk.CTkTextbox(
    main_frame,
    width=700,
    height=400
)

chat_box.pack(pady=10)

entry = ctk.CTkEntry(
    main_frame,
    width=600
)

entry.pack(pady=10)

send_button = ctk.CTkButton(
    main_frame,
    text="Send",
    command=send_message
)

send_button.pack(pady=10)

voice_button = ctk.CTkButton(
    main_frame,
    text="🎤 Speak",
    command=voice_message
)

voice_button.pack(pady=10)

entry.bind(
    "<Return>",
    lambda event: send_message()
)

def on_close():
    window.withdraw()

window.protocol(
    "WM_DELETE_WINDOW",
    on_close
)

Thread(
    target=ai_worker,
    daemon=True
).start()

Thread(
    target=wake_listener,
    args=(window, conversation_mode),
    daemon=True
).start()
run_tray(window)

window.mainloop()
