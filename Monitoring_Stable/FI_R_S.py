import datetime
import time
import csv
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
from pymongo import MongoClient

from Model_Handler.handler import predict_file_access

# File to save logs
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"Records/file_access_log/file_access_log_{formatted_time}.csv"

EXCLUDED_PATH = "/Users/thenethsanjukatheneth/Documents/MSC_/Records"

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]
collection = db["File_abnormalities"]


# Check if the log file exists, if not, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'event_type', 'file_path', 'time', 'is_directory', 'hash'
        ])
        writer.writeheader()


# Append logs to the file
def append_log(event_type, file_path, is_directory, file_hash=None):
    data = [{
        'event_type': event_type,
        'file_path': file_path,
        'time': time.time(),
        'is_directory': is_directory,
        'hash': file_hash
    }]

    # Predict and filter for "Normal"
    predictions = predict_file_access(data)
    if predictions[0] == "Normal":
        with open(LOG_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'event_type', 'file_path', 'time', 'is_directory', 'hash'
            ])
            writer.writerows(data)
    else:
        data_abnormal = {
            'event_type': event_type,
            'file_path': file_path,
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_directory': is_directory,
            'hash': file_hash
        }
        collection.insert_one(data_abnormal)




# Calculate file hash
def calculate_file_hash(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None


# Custom event handler
class FileEventHandler(FileSystemEventHandler):
    known_files = {}

    def should_ignore(self, path):
        """Check if the event path is inside the excluded path."""
        return path.startswith(EXCLUDED_PATH)

    def on_created(self, event):
        if self.should_ignore(event.src_path):
            return

        if not event.is_directory:
            file_hash = calculate_file_hash(event.src_path)
            if file_hash in self.known_files.values():
                append_log('copy_detected', event.src_path, event.is_directory, file_hash)
            else:
                self.known_files[event.src_path] = file_hash
                append_log('created', event.src_path, event.is_directory, file_hash)

    def on_deleted(self, event):
        if self.should_ignore(event.src_path):
            return

        file_hash = self.known_files.pop(event.src_path, None)  # Remove from known_files if present
        append_log('deleted', event.src_path, event.is_directory, file_hash)

    def on_modified(self, event):
        if self.should_ignore(event.src_path):
            return

        if not event.is_directory:
            file_hash = calculate_file_hash(event.src_path)
            self.known_files[event.src_path] = file_hash
            append_log('modified', event.src_path, event.is_directory, file_hash)

    def on_moved(self, event):
        if self.should_ignore(event.src_path) or self.should_ignore(event.dest_path):
            return

        if event.src_path in self.known_files:
            self.known_files[event.dest_path] = self.known_files.pop(event.src_path)
        append_log('moved', event.dest_path, event.is_directory)


# File monitoring function
def start_file_monitoring(path_to_watch):
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# Keyboard listener to stop the program on 'Escape' key
def start_keyboard_listener():
    from pynput import keyboard

    def on_press(key):
        global stop_logging
        if key == keyboard.Key.esc:
            stop_logging = True
            return False  # Stop the keyboard listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    directory_to_watch = "."  # Change this to the directory you want to monitor
    stop_logging = False

    print("Starting file access logger.")
    # Start file monitoring in a thread
    file_thread = Thread(target=start_file_monitoring, args=(directory_to_watch,))
    file_thread.daemon = True  # Run as a background thread
    file_thread.start()

    # Start the keyboard listener in the main thread
    try:
        start_keyboard_listener()
    except KeyboardInterrupt:
        print("\nStopping file monitor.")
