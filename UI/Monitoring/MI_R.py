import datetime
import time
import math
import csv
import os
from pynput import mouse, keyboard
from threading import Thread

# File to save logs
# Get the current date and time
current_time = datetime.datetime.now()

# Format the date and time as desired (e.g., YYYY-MM-DD_HH-MM-SS)
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# Construct the log file name with the date and time
LOG_FILE = f"Records/mouse_data_log/mouse_data_log_{formatted_time}.csv"

# Check if the log file exists, if not, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'event', 'x', 'y', 'speed', 'button', 'time', 'scroll', 'session_id'
        ])
        writer.writeheader()

# Variables to track session
current_session_id = int(time.time())
stop_logging = False  # Global flag to stop logging

# Variables for speed calculation
last_x, last_y, last_time = None, None, None


# Event logging function
def log_event(event, x=None, y=None, speed=None, button=None, scroll=None):
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'event', 'x', 'y', 'speed', 'button', 'time', 'scroll', 'session_id'
        ])
        writer.writerow({
            'event': event,
            'x': x,
            'y': y,
            'speed': speed,
            'button': button,
            'time': time.time(),
            'scroll': scroll,
            'session_id': current_session_id
        })


# Mouse event callbacks
def on_move(x, y):
    global last_x, last_y, last_time
    if not stop_logging:
        current_time = time.time()

        # Calculate speed if previous position exists
        if last_x is not None and last_y is not None and last_time is not None:
            distance = math.sqrt((x - last_x) ** 2 + (y - last_y) ** 2)  # Euclidean distance
            time_diff = current_time - last_time
            speed = distance / time_diff if time_diff > 0 else 0
        else:
            speed = 0  # Initial movement speed

        # Log the event
        log_event('move', x=x, y=y, speed=speed)

        # Update last position and time
        last_x, last_y, last_time = x, y, current_time


def on_click(x, y, button, pressed):
    if not stop_logging:
        event_type = 'click_press' if pressed else 'click_release'
        log_event(event_type, x=x, y=y, button=str(button))


def on_scroll(x, y, dx, dy):
    if not stop_logging:
        log_event('scroll', x=x, y=y, scroll=(dx, dy))


# Start the mouse listener
def start_mouse_logging():
    global stop_logging
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        while not stop_logging:
            time.sleep(0.1)  # Prevent CPU overuse
        listener.stop()


# Keyboard listener to stop the program on 'Escape' key
def start_keyboard_listener():
    global stop_logging

    def on_press(key):
        global stop_logging
        if key == keyboard.Key.esc:
            stop_logging = True
            return False  # Stop the keyboard listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    # Start mouse and keyboard listeners in separate threads
    print("Starting background mouse logger.")
    mouse_thread = Thread(target=start_mouse_logging)
    mouse_thread.daemon = True  # Run as a background thread
    mouse_thread.start()

    # Start the keyboard listener in the main thread
    try:
        start_keyboard_listener()
    except KeyboardInterrupt:
        print("")
