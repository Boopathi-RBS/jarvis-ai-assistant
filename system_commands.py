from datetime import datetime
from permissions import has_permission
import psutil

def process_system_command(message):
    msg = message.lower()
    now = datetime.now()

    if "date" in msg:
        return now.strftime("Today is %d %B %Y.")

    elif "time" in msg:
        return now.strftime("The current time is %I:%M %p.")

    elif "day" in msg:
        return now.strftime("Today is %A.")

    elif "month" in msg:
        return now.strftime("Current month is %B.")

    elif "year" in msg:
        return now.strftime("Current year is %Y.")

    elif "battery" in msg:

        if not has_permission("battery"):
            return "Battery permission is disabled."

        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery information is not available."

        if battery.power_plugged:
            return f"Battery is {battery.percent}% and charging."

        return f"Battery is {battery.percent}%."
    
    elif "cpu" in msg:

        if not has_permission("cpu"):
            return "CPU permission is disabled."

        cpu = psutil.cpu_percent(interval=1)

        return f"CPU usage is {cpu} percent."
    
    elif "ram" in msg or "memory usage" in msg:

        if not has_permission("ram"):
            return "RAM permission is disabled."

        memory = psutil.virtual_memory()

        return f"RAM usage is {memory.percent} percent."
    
    elif "disk" in msg or "storage" in msg:

        if not has_permission("disk"):
            return "Disk permission is disabled."

        disk = psutil.disk_usage("/")

        total = round(disk.total / (1024**3), 2)
        used = round(disk.used / (1024**3), 2)
        free = round(disk.free / (1024**3), 2)

        return (
            f"Disk usage is {disk.percent}%.\n"
            f"Total: {total} GB\n"
            f"Used: {used} GB\n"
            f"Free: {free} GB"
        )

    return None