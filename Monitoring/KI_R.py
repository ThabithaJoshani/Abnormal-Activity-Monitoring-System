import datetime
import time
import csv
import os
from pynput import keyboard
from threading import Thread

# File to save logs
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"Records/key_log/key_log_{formatted_time}.csv"

# Check if the log file already exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'key', 'event', 'time', 'press_duration', 'release_time',
            'inter_key_interval', 'session_id'
        ])
        writer.writeheader()

# Thread-safe logging variables
key_logs = []
last_release_time = None
current_session_id = int(time.time())  # Unique session ID for this instance


# Append logs to the file
def append_logs(logs):
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'key', 'event', 'time', 'press_duration', 'release_time',
            'inter_key_interval', 'session_id'
        ])
        writer.writerows(logs)


# Listener functions
def on_press(key):
    global last_release_time
    try:
        key_logs.append({
            'key': key.char,
            'event': 'press',
            'time': time.time(),
            'press_duration': None,
            'release_time': None,
            'inter_key_interval': time.time() - last_release_time if last_release_time else None,
            'session_id': current_session_id
        })
    except AttributeError:
        # Handle special keys (e.g., Shift, Ctrl, etc.)
        key_logs.append({
            'key': str(key),
            'event': 'press',
            'time': time.time(),
            'press_duration': None,
            'release_time': None,
            'inter_key_interval': time.time() - last_release_time if last_release_time else None,
            'session_id': current_session_id
        })


def on_release(key):
    global last_release_time
    release_time = time.time()
    try:
        # Match the release event with the last press of the same key
        for log in reversed(key_logs):
            if log['key'] == key.char and log['event'] == 'press' and log['press_duration'] is None:
                log['press_duration'] = release_time - log['time']
                log['release_time'] = release_time
                break
    except AttributeError:
        # Handle special keys (e.g., Shift, Ctrl, etc.)
        for log in reversed(key_logs):
            if log['key'] == str(key) and log['event'] == 'press' and log['press_duration'] is None:
                log['press_duration'] = release_time - log['time']
                log['release_time'] = release_time
                break

    # Update the last release time
    last_release_time = release_time

    # Save logs periodically
    if len(key_logs) >= 20:  # Save logs every 20 events
        append_logs(key_logs[:20])
        del key_logs[:20]

    # Stop the script when "Escape" is pressed
    if key == keyboard.Key.esc:
        append_logs(key_logs)  # Save remaining logs
        return False


# Start the keyboard listener in a thread
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    print("Starting enhanced key logger. Press 'Escape' to stop.")
    listener_thread = Thread(target=start_listener)
    listener_thread.daemon = True  # Run as a background thread
    listener_thread.start()

    # Keep the script running
    try:
        while listener_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping key logger.")
