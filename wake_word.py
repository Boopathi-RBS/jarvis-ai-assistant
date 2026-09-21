from voice_input import listen
from voice_output import speak


def wake_listener(window):

    print("Boopathi AI wake listener started.")
    print('Say "Hey Boopathi"')

    while True:

        try:

            text = listen()

            if not text:
                continue

            text = text.lower().strip()

            print("Wake listener heard:", text)

            if "hey boopathi" in text:

                print("Wake word detected!")

                speak("Yes sir")

                window.after(
                    0,
                    show_window,
                    window
                )

        except Exception as e:

            print("Wake listener error:", e)


def show_window(window):

    window.deiconify()
    window.lift()
    window.focus_force()