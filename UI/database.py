from pymongo import MongoClient
import pandas as pd
import os

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]

# Load collections
file_access_collection = db["File_abnormalities"]
keyboard_collection = db["Keyboard_abnormalities"]
mouse_collection = db["Mouse_abnormalities"]
IP_collection = db["IP_abnormalities"]

# File paths
paths = {
    "file_access": "Records/file_access_log/trained",
    "keyboard": "Records/key_log/trained",
    "mouse": "Records/mouse_data_log/trained",
    "ip": "Records/ip_change_log/trained"
}

# Ensure directories exist
for key, path in paths.items():
    if not os.path.exists(path):
        print(f"Directory '{path}' does not exist. Creating it...")
        os.makedirs(path)


# Function to read CSV files from a directory
def load_csv_from_directory(directory_path):
    all_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(".csv")]
    if not all_files:
        print(f"No CSV files found in directory: {directory_path}. Returning an empty DataFrame.")
        return pd.DataFrame()
    return pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)


# Insert data into MongoDB
def insert_data_to_collection(dataframe, collection, collection_name):
    if dataframe.empty:
        print(f"No data available to insert into {collection_name} collection.")
        return

    records = dataframe.to_dict(orient="records")
    result = collection.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} documents into {collection_name} collection.")


# Load and insert data for file access logs
file_access_data = load_csv_from_directory(paths["file_access"])
insert_data_to_collection(file_access_data, file_access_collection, "File Access")

# Load and insert data for key log data
keyboard_data = load_csv_from_directory(paths["keyboard"])
insert_data_to_collection(keyboard_data, keyboard_collection, "Keyboard")

# Load and insert data for mouse data
mouse_data = load_csv_from_directory(paths["mouse"])
insert_data_to_collection(mouse_data, mouse_collection, "Mouse")

# Load and insert data for IP change logs
ip_data = load_csv_from_directory(paths["ip"])
insert_data_to_collection(ip_data, IP_collection, "IP")

print("Data insertion completed.")
