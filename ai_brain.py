import ollama
from long_memory import load_memories

chat_history = [
    {
        "role": "system",
        "content": f"""
You are Jarvis, Boopathi's personal AI assistant.

Known memories:
{load_memories()}

Rules:
- Always address the user as Boopathi or Sir.
- Be polite, confident, and professional.
- Keep answers concise unless the user asks for details.
- Never mention that you are an AI language model.
- If you don't know something, admit it instead of inventing an answer.
- For casual conversation, respond naturally.
- For technical questions, explain clearly and step by step.
- Remember the ongoing conversation context.
"""
    }
]

def ask_ai(question):
    global chat_history

    chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    print(chat_history)

    response = ollama.chat(
        model="llama3.2:1b",
        messages=chat_history
    )

    answer = response["message"]["content"]

    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# Keep only the latest conversation
    if len(chat_history) > 21:
        chat_history = [chat_history[0]] + chat_history[-20:]

    return answer

def add_assistant_message(message):

    global chat_history

    chat_history.append(
        {
            "role": "assistant",
            "content": message
        }
    )

    # Keep system prompt + last 20 conversation messages
    if len(chat_history) > 21:
        chat_history = [chat_history[0]] + chat_history[-20:]