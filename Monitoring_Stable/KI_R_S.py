import datetime
import time
import csv
import os

from pymongo import MongoClient
from pynput import keyboard
from threading import Thread
import pandas as pd

from Model_Handler.handler import predict_key_log

# File to save log
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"Records/key_log/key_log_{formatted_time}.csv"

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]
collection = db["Keyboard_abnormalities"]

# Check if the log file already exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'key', 'event', 'time', 'press_duration', 'release_time',
            'inter_key_interval', 'session_id'
        ])
        writer.writeheader()

# Thread-safe logging variables
last_release_time = None
current_session_id = int(time.time())


# Real-time prediction and logging function
def process_log(log):
    """
    Predict and save logs in real-time.
    """
    # Ensure only necessary fields are used for prediction
    required_fields = ["time", "press_duration", "inter_key_interval"]

    # Convert the log to a DataFrame for prediction
    log_df = pd.DataFrame([log])

    # Verify all required fields are present
    if not all(field in log_df.columns for field in required_fields):
        print("Log does not contain all required fields for prediction. Skipping.")
        return

    # Select only the required fields for prediction
    prediction_input = log_df[required_fields]
    prediction_input = prediction_input.fillna(0.5)
    prediction_input = prediction_input.infer_objects(copy=False)

    # Predict using the handler
    try:

        predictions = predict_key_log(prediction_input)
        log_df['prediction'] = predictions

        # Handle predictions
        if predictions[0] == "Normal":
            log_df = log_df.drop(columns=['prediction'])  # Drop prediction column if not needed
            with open(LOG_FILE, 'a', newline='') as file:
                log_df.to_csv(file, index=False, header=False)
        else:
            # Handle "Abnormal" logs (e.g., log to console or alert)
            dft = log_df
            dft["time"] = time.strftime('%Y-%m-%d %H:%M:%S')
            collection.insert_one(dft)

    except Exception as e:
        print(f"Error during prediction: {e}")


# Listener functions
def on_press(key):
    global last_release_time
    try:
        log = {
            'key': key.char,
            'event': 'press',
            'time': time.time(),
            'press_duration': None,
            'release_time': None,
            'inter_key_interval': time.time() - last_release_time if last_release_time else None,
            'session_id': current_session_id
        }
    except AttributeError:
        # Handle special keys (e.g., Shift, Ctrl, etc.)
        log = {
            'key': str(key),
            'event': 'press',
            'time': time.time(),
            'press_duration': None,
            'release_time': None,
            'inter_key_interval': time.time() - last_release_time if last_release_time else None,
            'session_id': current_session_id
        }

    # Process the log immediately for real-time prediction
    process_log(log)


def on_release(key):
    global last_release_time
    release_time = time.time()

    try:
        # Create a release log
        log = {
            'key': key.char if hasattr(key, 'char') else str(key),
            'event': 'release',
            'time': time.time(),
            'press_duration': None,  # Update if duration tracking is needed
            'release_time': release_time,
            'inter_key_interval': None,  # No interval for release events
            'session_id': current_session_id
        }
    except AttributeError:
        # Handle special keys (e.g., Shift, Ctrl, etc.)
        log = {
            'key': str(key),
            'event': 'release',
            'time': time.time(),
            'press_duration': None,
            'release_time': release_time,
            'inter_key_interval': None,
            'session_id': current_session_id
        }

    # Process the log immediately for real-time prediction
    process_log(log)

    # Update the last release time
    last_release_time = release_time

    # Stop the script when "Escape" is pressed
    if key == keyboard.Key.esc:
        print("ESC key pressed. Stopping the logger.")
        return False


# Start the keyboard listener in a thread
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    print("Starting real-time key logger. Press 'Escape' to stop.")
    listener_thread = Thread(target=start_listener)
    listener_thread.daemon = True  # Run as a background thread
    listener_thread.start()

    # Keep the script running
    try:
        while listener_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping key logger.")
