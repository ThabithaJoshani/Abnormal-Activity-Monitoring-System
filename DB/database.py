from pymongo import MongoClient
import pandas as pd

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]

# Load collections
file_access_collection = db["File_abnormalities"]
keyboard_collection = db["Keyboard_abnormalities"]
mouse_collection = db["Mouse_abnormalities"]
IP_collection = db["IP_abnormalities"]

Sample_file_access_log_data_csv = "UI/Records/file_access_log/trained"

# Sample data
sample_file_access_data = pd.DataFrame({
    "event_type": ["created", "modified"],
    "file_path": ["/path/to/file1", "/path/to/file2"],
    "time": [1733545091.5, 1733545100.2],
    "is_directory": [0, 0]
})

# Key Log Prediction
sample_key_log_data = pd.DataFrame({
    "time": [1733545091.5, 1733545100.2],
    "press_duration": [0.5, 0.6],
    "inter_key_interval": [0.1, 0.2]
})

# Mouse Data Log Prediction
sample_mouse_data = pd.DataFrame({
    "x": [50, 100],
    "y": [60, 200],
    "speed": [0.5, 1.0],
    "button": ["left", "right"],
    "time": [1733545091.5, 1733545100.2],
    "scroll": ["up", "down"]
})

# Convert DataFrame to list of dictionaries
records_file_access_data = sample_file_access_data.to_dict(orient="records")
records_key_log_data = sample_key_log_data.to_dict(orient="records")
records_mouse_data = sample_mouse_data.to_dict(orient="records")

# Insert data into MongoDB
result1 = file_access_collection.insert_many(records_file_access_data)
result2 = keyboard_collection.insert_many(records_key_log_data)
result3 = mouse_collection.insert_many(records_mouse_data)

# Print inserted IDs
print(f"Inserted document IDs: {result1.inserted_ids}")
print(f"Inserted document IDs: {result2.inserted_ids}")
print(f"Inserted document IDs: {result3.inserted_ids}")

