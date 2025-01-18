import time
import csv
import os
import socket
from datetime import datetime
from threading import Thread
import requests
from pynput import keyboard

# File to save logs
# Get the current date and time
current_time = datetime.now()

# Format the date and time
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# Construct the log file name with the date and time
LOG_FILE = f"Records/ip_change_log/ip_change_log_{formatted_time}.csv"

# Check if the log file exists, if not, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'timestamp', 'event_type', 'ip_address', 'host_name'
        ])
        writer.writeheader()


# Append logs to the file
def append_log(event_type, ip_address, host_name):
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'timestamp', 'event_type', 'ip_address', 'host_name'
        ])
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'ip_address': ip_address,
            'host_name': host_name
        })


# Calculate the current public IP address
def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching IP: {e}")
    return None


# Get the host name of the device
def get_host_name():
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error fetching hostname: {e}")
    return "Unknown"


# Monitor IP changes
def monitor_ip_changes(interval=60):
    global stop_monitoring
    current_ip = None
    while not stop_monitoring:
        new_ip = get_current_ip()
        if new_ip and new_ip != current_ip:
            if current_ip is None:
                append_log('initial_ip', new_ip, get_host_name())
            else:
                append_log('ip_changed', new_ip, get_host_name())
            current_ip = new_ip
        time.sleep(interval)


# Keyboard listener to stop the monitoring with the Esc key
def start_keyboard_listener():
    def on_press(key):
        global stop_monitoring
        if key == keyboard.Key.esc:
            stop_monitoring = True
            return False  # Stop the keyboard listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    # Global variable to control monitoring
    stop_monitoring = False

    print("Starting IP monitoring.")

    # Start the IP monitoring in a thread
    ip_thread = Thread(target=monitor_ip_changes, args=(60,))
    ip_thread.daemon = True
    ip_thread.start()

    # Start the keyboard listener in the main thread
    start_keyboard_listener()

    # Wait for the IP thread to finish
    ip_thread.join()
    print("IP monitoring stopped.")
