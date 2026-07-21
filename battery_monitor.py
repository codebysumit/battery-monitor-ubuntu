#!/usr/bin/env python3
"""
Battery Monitor for Ubuntu
---------------------------
This script checks your laptop battery every 60 seconds.

Rule 1: If battery <= 35% and NOT charging -> show low battery popup
Rule 2: If battery >= 75% and IS charging -> show overcharge popup

It will not repeat the same popup again and again.
It only shows it once, then waits until the condition resets.
"""

import psutil
import subprocess
import threading
import time
import os
from datetime import datetime

# how often to check (in seconds)
CHECK_EVERY = 60

# battery limits
LOW_LIMIT = 35
HIGH_LIMIT = 75

# sound file that will beep. This file exists on most Ubuntu systems.
SOUND_FILE = "/usr/share/sounds/freedesktop/stereo/dialog-warning.oga"

# log file will be saved in your home folder
LOG_FILE = os.path.expanduser("~/battery_monitor.log")


def log_event(message):
    """Write a line to the log file with date and time."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line.strip())


def beep_loop(stop_event):
    """Keep playing beep sound every 1.5 sec until stop_event is set."""
    while not stop_event.is_set():
        subprocess.run(["paplay", SOUND_FILE])
        time.sleep(1.5)


def send_popup(title, message):
    """
    Show a popup with OK button using zenity.
    Beep sound plays on loop until user clicks OK.
    This function blocks (waits) until OK is clicked.
    Also sends a quick notification and writes to log file.
    """
    # quick notification (top corner, auto disappears)
    subprocess.run(["notify-send", "-u", "critical", "-i", "battery", title, message])

    # write this event to the log file
    log_event(f"{title} - {message.splitlines()[0]}")

    stop_event = threading.Event()

    # start beeping in background thread
    sound_thread = threading.Thread(target=beep_loop, args=(stop_event,))
    sound_thread.start()

    # show popup box with OK button. This line waits until user clicks OK.
    subprocess.run([
        "zenity", "--warning",
        "--title", title,
        "--text", message,
        "--width", "300"
    ])

    # user clicked OK, stop the beeping
    stop_event.set()
    sound_thread.join()
    log_event(f"Popup closed by user - {title}")

def main():
    # flags to remember if we already sent a warning
    low_warned = False
    high_warned = False

    print("Battery monitor started. Watching your battery level...")
    log_event("Battery monitor script started")

    while True:
        battery = psutil.sensors_battery()

        if battery is None:
            print("No battery found. This might be a desktop PC.")
            time.sleep(CHECK_EVERY)
            continue

        percent = battery.percent
        charging = battery.power_plugged

        # ---- Rule 1: LOW battery, discharging ----
        if percent <= LOW_LIMIT and not charging:
            if not low_warned:
                send_popup(
                    "Battery Low!",
                    f"Battery is at {percent}%. Please charge it now.\n"
                    f"Deep discharge is bad for battery health."
                )
                low_warned = True
        else:
            # reset flag once battery goes above low limit or starts charging
            low_warned = False

        # ---- Rule 2: HIGH battery, charging ----
        if percent >= HIGH_LIMIT and charging:
            if not high_warned:
                send_popup(
                    "Battery Almost Full!",
                    f"Battery is at {percent}%. Unplug the charger now.\n"
                    f"Overcharging reduces battery lifespan."
                )
                high_warned = True
        else:
            # reset flag once battery drops below high limit or unplugged
            high_warned = False

        time.sleep(CHECK_EVERY)

if __name__ == "__main__":
    main()
