# config.py

# ==========================================
# BOOPATHI AI CONFIGURATION
# ==========================================

# -----------------------------
# AI
# -----------------------------

AI_MODEL = "llama3.2:1b"


# -----------------------------
# Voice
# -----------------------------

VOICE_NAME = "en-US-GuyNeural"

WAKE_PHRASES = [
    "hey boopathi",
    "hey jarvis"
]


# -----------------------------
# Microphone
# -----------------------------

SAMPLE_RATE = 44100

CHANNELS = 1

RECORD_DURATION = 5


# -----------------------------
# Conversation
# -----------------------------

MAX_CONVERSATION_HISTORY = 20

MAX_SILENCE_ATTEMPTS = 4


# -----------------------------
# Assistant
# -----------------------------

ASSISTANT_NAME = "JARVIS AI"

USER_NAME = "Boopathi"


# -----------------------------
# Files
# -----------------------------

RECORDING_FILE = "recording.wav"

PERMISSION_FILE = "permissions.json"


# -----------------------------
# Debug
# -----------------------------

DEBUG = True