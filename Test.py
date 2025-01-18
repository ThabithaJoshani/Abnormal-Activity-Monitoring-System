# File Access Log Prediction
import pandas as pd

from Model_Handler.handler import predict_file_access, predict_key_log, predict_mouse_data
# File Access Log Prediction
sample_file_access_data = pd.DataFrame({
    "event_type": ["created", "modified"],
    "file_path": ["/path/to/file1", "/path/to/file2"],
    "time": [1733545091.5, 1733545100.2],
    "is_directory": [0, 0]
})
print("File Access Predictions:", predict_file_access(sample_file_access_data))

# Key Log Prediction
sample_key_log_data = pd.DataFrame({
    "time": [1733545091.5, 1733545100.2],
    "press_duration": [0.5, 0.6],
    "inter_key_interval": [0.1, 0.2]
})
print("Key Log Predictions:", predict_key_log(sample_key_log_data))

# Mouse Data Log Prediction
sample_mouse_data = pd.DataFrame({
    "x": [50, 100],
    "y": [60, 200],
    "speed": [0.5, 1.0],
    "button": ["left", "right"],
    "time": [1733545091.5, 1733545100.2],
    "scroll": ["up", "down"]
})
print("Mouse Data Predictions:", predict_mouse_data(sample_mouse_data))