#!/bin/bash
# system_requirements.sh
# Installs system tools needed by battery_monitor.py
# (these are not Python packages, so pip cannot install them)

echo "Installing system requirements..."
sudo apt update
sudo apt install -y python3 python3-pip python3-psutil zenity libnotify-bin pulseaudio-utils

echo "Done. python3, psutil, pip, zenity, notify-send, and paplay are now ready."
