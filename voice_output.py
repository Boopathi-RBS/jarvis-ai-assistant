import asyncio
import edge_tts
import tempfile
import os
import vlc
from threading import Event

VOICE = "en-US-GuyNeural"

stop_event = Event()

player = None


def speak(text):

    stop_event.clear()

    if not text:
        return

    async def _speak():

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as f:

            filename = f.name

        communicate = edge_tts.Communicate(
            text=text,
            voice=VOICE
        )

        await communicate.save(filename)

        global player

        player = vlc.MediaPlayer(filename)

        player.play()

        # Wait until playback starts
        while player.get_state() != vlc.State.Playing:

            if stop_event.is_set():
                player.stop()
                break

            await asyncio.sleep(0.05)

        # Wait until playback finishes
        while player.is_playing():

            if stop_event.is_set():

                player.stop()
                break

            await asyncio.sleep(0.1)

        player.release()

        os.remove(filename)

    asyncio.run(_speak())
    
def stop_speaking():

    global player

    stop_event.set()

    if player is not None:

        try:
            player.stop()
            player.release()
        except Exception:
            pass

        player = None