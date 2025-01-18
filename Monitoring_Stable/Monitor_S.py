import threading
from FI_R_S import start_file_monitoring
from IPI_R_S import monitor_ip_changes, start_keyboard_listener as ip_listener
from KI_R_S import start_listener as key_logger
from MI_R_S import start_mouse_logging


# Define functions to run each monitoring script in a thread
def run_file_monitoring(path_to_watch):
    print("Starting file monitoring...")
    start_file_monitoring(path_to_watch)


def run_ip_monitoring():
    print("Starting IP monitoring...")
    monitor_ip_changes(interval=60)


def run_key_logging():
    print("Starting key logging...")
    key_logger()


def run_mouse_logging():
    print("Starting mouse logging...")
    start_mouse_logging()


if __name__ == "__main__":
    print("Main Monitoring Script")
    print("Press 'Escape' to stop all monitoring.")

    # Define threads for each script
    file_monitor_thread = threading.Thread(target=run_file_monitoring, args=(".",))
    ip_monitor_thread = threading.Thread(target=run_ip_monitoring)
    key_log_thread = threading.Thread(target=run_key_logging)
    mouse_log_thread = threading.Thread(target=run_mouse_logging)

    # Start all threads
    file_monitor_thread.start()
    ip_monitor_thread.start()
    key_log_thread.start()
    mouse_log_thread.start()

    # Start the IP listener to terminate on 'Escape'
    try:
        ip_listener()  # Use the IP listener as the master listener for global termination
    except KeyboardInterrupt:
        print("\nStopping all monitors...")

    # Ensure all threads stop gracefully
    file_monitor_thread.join()
    ip_monitor_thread.join()
    key_log_thread.join()
    mouse_log_thread.join()

    print("All monitoring stopped.")
