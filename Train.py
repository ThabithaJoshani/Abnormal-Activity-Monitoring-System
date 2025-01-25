import os
import glob
import shutil
from Training.training_autoencoder import train_or_update_autoencoder
from Training.training_ip_changers_RandomForestClassifier import load_logs, preprocess_logs, train_or_update_random_forest
from Training.training_isolation_forest import train_or_update_isolation_forest
from Training.training_one_class_svm import train_or_update_one_class_svm


# Directories to process
DIRECTORIES = {
    "file_access_log": "Records/file_access_log",
    "key_log": "Records/key_log",
    "mouse_data_log": "Records/mouse_data_log",
    "ip_change_log": "Records/ip_change_log"
}

# Central directory for saving models
MODELS_DIR = "Models"

# Ensure Models directory exists
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# Process each directory
# Create 'trained' subdirectories if not exist
for dir_type, path in DIRECTORIES.items():
    trained_path = os.path.join(path, "trained")
    if not os.path.exists(trained_path):
        os.makedirs(trained_path)

# Process each directory
for dir_type, path in DIRECTORIES.items():
    print(f"Processing {dir_type}...")

    # Collect all CSV files
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if not csv_files:
        print(f"No files found in {path}. Skipping...")
        continue

    try:
        # Define save path for the model
        model_save_path = os.path.join(MODELS_DIR, dir_type)
        if not os.path.exists(model_save_path):
            os.makedirs(model_save_path)
        print(f"Model save path: {model_save_path}")

        # Call the appropriate training function
        if dir_type == "file_access_log":
            train_or_update_isolation_forest(path, model_save_path)
        elif dir_type == "key_log":
            train_or_update_one_class_svm(path, model_save_path)
        elif dir_type == "mouse_data_log":
            train_or_update_autoencoder(path, model_save_path)
        elif dir_type == "ip_change_log":
            logs = load_logs(os.path.join(path, "*.csv"))
            data = preprocess_logs(logs)
            train_or_update_random_forest(data, model_save_path)

        # Move processed files to 'trained' folder
        for file in csv_files:
            shutil.move(file, os.path.join(path, "trained", os.path.basename(file)))

        print(f"Finished processing {dir_type}.")
    except Exception as e:
        print(f"Error during training for {dir_type}: {e}")
