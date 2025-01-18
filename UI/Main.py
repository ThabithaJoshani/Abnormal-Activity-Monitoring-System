import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from threading import Thread
from pynput import keyboard

# Configuration file path
CONFIG_FILE = "../config.json"

# Default configuration (used if config.json does not exist)
DEFAULT_CONFIG = {
    "initiated_date": None,
    "learning_period_days": 7,  # Default learning period
    "train_frequency": 3600,  # Frequency for Train.py (in seconds)
    "monitor_frequency": 1800,  # Frequency for Monitor.py and Monitor_S.py (in seconds)
}

# Global stop flag
stop_script = False


# Load or create configuration
def load_or_create_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        else:
            raise FileNotFoundError
    except (FileNotFoundError, json.JSONDecodeError):
        # Create a new configuration file if not found or invalid
        config = DEFAULT_CONFIG.copy()
        config["initiated_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        print("Configuration file created with default values.")
        return config


# Run a script as a subprocess
def run_script(script_name):
    try:
        print(f"Starting {script_name}...")
        process = subprocess.Popen(["python", script_name])
        return process
    except Exception as e:
        print(f"Error starting {script_name}: {e}")
        return None


# Stop a subprocess gracefully
def stop_process(process):
    if process and process.poll() is None:  # Check if the process is still running
        print(f"Stopping process {process.pid}...")
        process.terminate()
        process.wait()
        print(f"Process {process.pid} stopped.")


# Function to manage a script execution in a loop
def manage_script(script_name, frequency):
    while not stop_script:
        process = run_script(script_name)
        time.sleep(frequency)
        stop_process(process)


# Keyboard listener to stop the script
def keyboard_listener():
    global stop_script

    def on_press(key):
        global stop_script
        if key == keyboard.Key.esc:
            print("ESC key pressed. Stopping the script...")
            stop_script = True
            return False  # Stop the listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


# Main execution loop
def main():
    global stop_script
    config = load_or_create_config()
    initiated_date = datetime.strptime(config["initiated_date"], "%Y-%m-%d %H:%M:%S")
    learning_period_days = config["learning_period_days"]
    train_frequency = config["train_frequency"]
    monitor_frequency = config["monitor_frequency"]

    # Calculate the end of the learning period
    learning_period_end = initiated_date + timedelta(days=learning_period_days)

    while not stop_script:
        current_time = datetime.now()

        if current_time < learning_period_end:
            print("In learning period.")

            # Run Train.py and Monitor.py concurrently
            train_thread = Thread(target=manage_script, args=("Train.py", train_frequency))
            monitor_thread = Thread(target=manage_script, args=("Monitor.py", monitor_frequency))

            train_thread.start()
            monitor_thread.start()

            # Wait for the threads to complete
            train_thread.join()
            monitor_thread.join()

        else:
            print("Switching to monitoring mode.")

            # Run Train.py and Monitor_S.py concurrently
            train_thread = Thread(target=manage_script, args=("Train.py", train_frequency))
            monitor_s_thread = Thread(target=manage_script, args=("Monitor_S.py", monitor_frequency))

            train_thread.start()
            monitor_s_thread.start()

            # Wait for the threads to complete
            train_thread.join()
            monitor_s_thread.join()

        time.sleep(5)  # Short delay before next iteration


if __name__ == "__main__":
    # Start the keyboard listener in a separate thread
    listener_thread = Thread(target=keyboard_listener)
    listener_thread.daemon = True
    listener_thread.start()

    # Start the main script
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
    finally:
        print("Script terminated.")
