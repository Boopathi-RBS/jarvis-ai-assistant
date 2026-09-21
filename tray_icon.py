import pystray
from PIL import Image
from threading import Thread

def run_tray(window):

    image = Image.new(
        "RGB",
        (64, 64),
        color=(0, 120, 255)
    )

    def show_window(icon, item):
        
        window.after(
            0,
            lambda: (
                window.deiconify(),
                window.lift()
            )
        )
    def quit_app(icon, item):
        icon.stop()
        window.quit()

    menu = pystray.Menu(
        pystray.MenuItem(
            "Open Boopathi AI",
            show_window
        ),
        pystray.MenuItem(
            "Exit",
            quit_app
        )
    )

    icon = pystray.Icon(
        "BoopathiAI",
        image,
        "Boopathi AI",
        menu
    )

    Thread(
        target=icon.run,
        daemon=True
    ).start()