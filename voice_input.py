# voice_input.py

import os
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

from threading import Lock

from config import (
    SAMPLE_RATE,
    CHANNELS,
    RECORD_DURATION,
    RECORDING_FILE
)


# ==================================================
# MICROPHONE LOCK
# ==================================================

mic_lock = Lock()


# ==================================================
# SPEECH RECOGNIZER
# ==================================================

recognizer = sr.Recognizer()

# Adjust recognition sensitivity
recognizer.energy_threshold = 300

# Automatically adjust for small background noise
recognizer.dynamic_energy_threshold = True

# Seconds of silence before recognition considers
# the phrase finished (used by microphone APIs later)
recognizer.pause_threshold = 0.8


# ==================================================
# LISTEN
# ==================================================

def listen(duration=RECORD_DURATION):

    # ------------------------------------------------
    # Prevent multiple microphone sessions
    # ------------------------------------------------

    if not mic_lock.acquire(blocking=False):

        print(
            "[VOICE] Microphone is already in use."
        )

        return None

    try:

        print(
            "[VOICE] 🎤 Listening..."
        )

        # ------------------------------------------------
        # Record microphone
        # ------------------------------------------------

        recording = sd.rec(
            int(
                duration * SAMPLE_RATE
            ),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32"
        )

        sd.wait()

        # ------------------------------------------------
        # Save temporary recording
        # ------------------------------------------------

        sf.write(
            RECORDING_FILE,
            recording,
            SAMPLE_RATE
        )

        # ------------------------------------------------
        # Check recording
        # ------------------------------------------------

        if not os.path.exists(
            RECORDING_FILE
        ):

            print(
                "[VOICE] Recording file was not created."
            )

            return None

        # ------------------------------------------------
        # Speech recognition
        # ------------------------------------------------

        print(
            "[VOICE] 🧠 Recognizing..."
        )

        with sr.AudioFile(
            RECORDING_FILE
        ) as source:

            audio = recognizer.record(
                source
            )

        try:

            text = recognizer.recognize_google(
                audio
            )

        except sr.UnknownValueError:

            print(
                "[VOICE] ❌ Speech not understood."
            )

            return None

        except sr.RequestError as error:

            print(
                "[VOICE] ❌ Google recognition error:",
                error
            )

            return None

        # ------------------------------------------------
        # Clean result
        # ------------------------------------------------

        if not text:

            return None

        text = text.strip()

        if not text:

            return None

        print(
            f"[VOICE] ✅ Recognized: {text}"
        )

        return text

    except sd.PortAudioError as error:

        print(
            "[VOICE] ❌ Microphone error:",
            error
        )

        return None

    except Exception as error:

        print(
            "[VOICE] ❌ Unexpected voice error:",
            error
        )

        return None

    finally:

        # ------------------------------------------------
        # Always release microphone lock
        # ------------------------------------------------

        mic_lock.release()


# ==================================================
# DELETE TEMPORARY RECORDING
# ==================================================

def cleanup_recording():

    try:

        if os.path.exists(
            RECORDING_FILE
        ):

            os.remove(
                RECORDING_FILE
            )

            print(
                "[VOICE] Temporary recording removed."
            )

    except Exception as error:

        print(
            "[VOICE] Cleanup error:",
            error
        )