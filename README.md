# Battery Monitor for Ubuntu

A simple Python tool that watches your laptop battery level and warns you with a popup and sound alert when the battery is too low or overcharging. This helps protect your battery health over time.

## Features

- Checks battery percentage every 60 seconds
- Shows a **quick notification** in the corner of your screen
- Shows a **popup box with OK button** that keeps beeping until you click OK
- Warns you when battery is **35% or below** and not charging (low battery, deep discharge is bad for health)
- Warns you when battery is **75% or above** and charging (overcharge warning, unplug to protect battery life)
- Keeps a **log file** of all events with date and time
- Can **auto-start** every time you log in to Ubuntu

## Project Files

| File | Purpose |
|---|---|
| `battery_monitor.py` | Main Python script that checks battery and shows alerts |
| `system_requirements.sh` | Installs everything needed: python3, psutil, zenity, notify-send, paplay |
| `battery-monitor.service` | Systemd service file to auto-start the script on login |

## Requirements

- Ubuntu (or any Linux with GNOME desktop, tested on Ubuntu 24.04)
- Python 3
- `zenity`, `libnotify-bin`, `pulseaudio-utils` (system tools, not Python packages)

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/codebysumit/battery-monitor-ubuntu.git
cd battery-monitor
```

### 2. Install all requirements (system tools + Python packages)

This installs Python 3, psutil, zenity (popup boxes), notify-send (notifications), and paplay (sound). Everything comes through apt, no pip needed.

```bash
chmod +x system_requirements.sh
./system_requirements.sh
```

## Usage

### Run manually

```bash
python3 battery_monitor.py
```

Keep the terminal open, it will keep checking your battery every 60 seconds. Press `Ctrl+C` to stop it.

### Run automatically on every login (recommended)

This uses systemd so the script starts by itself in the background every time you log in to Ubuntu, no need to run it manually.

1. Copy the script to your home folder

```bash
cp battery_monitor.py ~/battery_monitor.py
```

2. Create the systemd user folder if it does not exist

```bash
mkdir -p ~/.config/systemd/user
```

3. Copy the service file there

```bash
cp battery-monitor.service ~/.config/systemd/user/
```

4. Reload systemd

```bash
systemctl --user daemon-reload
```

5. Enable it, so it starts on every login

```bash
systemctl --user enable battery-monitor.service
```

6. Start it right now (no need to reboot to test)

```bash
systemctl --user start battery-monitor.service
```

## Managing the Background Service

Check if it is running:

```bash
systemctl --user status battery-monitor.service
```

Stop it:

```bash
systemctl --user stop battery-monitor.service
```

Disable auto-start:

```bash
systemctl --user disable battery-monitor.service
```

See live logs from systemd:

```bash
journalctl --user -u battery-monitor.service -f
```

## Log File

All battery events are saved in a log file at:

```
~/battery_monitor.log
```

View it anytime:

```bash
cat ~/battery_monitor.log
```

Example content:

```
[2026-07-21 14:03:12] Battery monitor script started
[2026-07-21 15:22:05] Battery Low! - Battery is at 35%. Please charge it now.
[2026-07-21 15:22:41] Popup closed by user - Battery Low!
[2026-07-21 17:10:33] Battery Almost Full! - Battery is at 75%. Unplug the charger now.
```

## Configuration

You can change the battery limits by editing these lines at the top of `battery_monitor.py`:

```python
CHECK_EVERY = 60      # how often to check, in seconds
LOW_LIMIT = 35         # low battery warning percent
HIGH_LIMIT = 75        # overcharge warning percent
```

## Troubleshooting

**Popup or sound does not show up**

Test each tool one by one:

```bash
notify-send "Test" "Hello"
zenity --warning --text "Test popup"
paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga
```

If any command fails, re-run `system_requirements.sh`.

**No battery found message**

This script is made for laptops. Desktop PCs without a battery will show this message and skip the check.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Sumit Das
GitHub: [codebysumit](https://github.com/codebysumit)
