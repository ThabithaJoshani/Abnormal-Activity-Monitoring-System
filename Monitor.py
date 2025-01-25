import os
import subprocess
import time
from threading import Thread
from pynput import keyboard


main_dir = "Records"
sub_dirs = ["file_access_log", "key_log", "mouse_data_log", "ip_change_log"]

# Ensure the main directory exists
if not os.path.exists(main_dir):
    os.makedirs(main_dir)

# Ensure each subdirectory exists
for sub_dir in sub_dirs:
    full_path = os.path.join(main_dir, sub_dir)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

# Paths to the four scripts
SCRIPT_PATHS = [
    "Monitoring/FI_R.py",
    "Monitoring/IPI_R.py",
    "Monitoring/KI_R.py",
    "Monitoring/MI_R.py",
]

# Global flag to stop all threads
stop_all_scripts = False


# Function to run a script
def run_script(script_path):
    global stop_all_scripts
    process = None
    try:
        process = subprocess.Popen(["python", script_path])
        # Continuously check if stop flag is set
        while not stop_all_scripts:
            time.sleep(1)  # Check periodically
    except Exception as e:
        print(f"Error occurred while running {script_path}: {e}")
    finally:
        if process:
            process.terminate()  # Terminate the subprocess
            print(f"|-Stopped {script_path}")


# Function to listen for `Esc` key to stop all threads
def listen_for_esc():
    global stop_all_scripts

    def on_press(key):
        global stop_all_scripts
        if key == keyboard.Key.esc:
            print("Escape key pressed. Stopping all scripts.")
            stop_all_scripts = True
            return False  # Stop the listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    # Create and start a thread for each script
    threads = []
    for script in SCRIPT_PATHS:
        thread = Thread(target=run_script, args=(script,))
        thread.daemon = True  # Ensure threads exit when the main program exits
        threads.append(thread)
        thread.start()

    # Start the keyboard listener for stopping the scripts
    print("All scripts are running in separate threads. Press 'Esc' to stop.")
    esc_listener_thread = Thread(target=listen_for_esc)
    esc_listener_thread.start()

    # Wait for all threads to finish
    try:
        for thread in threads:
            thread.join()
        esc_listener_thread.join()
    except KeyboardInterrupt:
        print("\nForce stopping all scripts.")
        stop_all_scripts = True
