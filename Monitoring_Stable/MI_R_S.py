import datetime
import time
import math
import csv
import os

from pymongo import MongoClient
from pynput import mouse, keyboard
from threading import Thread

import pandas as pd

from Model_Handler.handler import predict_mouse_data

# File to save logs
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"Records/mouse_data_log/mouse_data_log_{formatted_time}.csv"

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]
collection = db["Mouse_abnormalities"]

# Check if the log file exists, if not, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'event', 'x', 'y', 'speed', 'button', 'time', 'scroll', 'session_id'
        ])
        writer.writeheader()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]
collection = db["File_abnormalities"]

# Variables to track session
current_session_id = int(time.time())
stop_logging = False  # Global flag to stop logging

# Variables for speed calculation
last_x, last_y, last_time = None, None, None

# Buffer to store events before prediction
event_buffer = []


# Event logging function
def log_event(event, x=None, y=None, speed=None, button=None, scroll=None):
    global event_buffer

    # Create a new event dictionary
    event_data = {
        'event': event,
        'x': x,
        'y': y,
        'speed': speed,
        'button': button,
        'time': time.time(),
        'scroll': scroll,
        'session_id': current_session_id
    }
    event_buffer.append(event_data)

    # Process and predict results in batches
    if len(event_buffer) >= 20:  # Adjust batch size as needed
        process_and_save_events()


def process_and_save_events():
    """
    Processes the event buffer, predicts results, and saves only "Normal" events.
    """
    global event_buffer

    # Convert the buffer to a DataFrame
    event_df = pd.DataFrame(event_buffer)

    # Predict using the handler
    if not event_df.empty:
        predictions = predict_mouse_data(event_df)
        event_df['prediction'] = predictions
        abnormal_events = event_df[event_df['prediction'] != "Normal"].drop(columns=['prediction'])
        # Filter "Normal" results
        normal_events = event_df[event_df['prediction'] == "Normal"].drop(columns=['prediction'])

        # Save only "Normal" events to the log file
        if not normal_events.empty:
            with open(LOG_FILE, 'a', newline='') as file:
                normal_events.to_csv(file, index=False, header=False)
        else:
            abnormal_events['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            collection.insert_one(abnormal_events)


    # Clear the buffer after processing
    event_buffer = []


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
