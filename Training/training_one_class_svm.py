from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def train_or_update_one_class_svm(data_path, save_path):
    """
    Train or update a One-Class SVM model for anomaly detection in key logs.

    :param data_path: Path to the directory containing CSV files.
    :param save_path: Path to save or load the trained model and scaler.
    """
    try:
        # Ensure save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Define file paths
        model_path = os.path.join(save_path, "key_svm_model.pkl")
        scaler_path = os.path.join(save_path, "key_scaler.pkl")

        # Read and combine all CSV files
        logging.info("Collecting CSV files...")
        all_files = [os.path.join(data_path, file) for file in os.listdir(data_path) if file.endswith('.csv')]
        if not all_files:
            logging.error("No CSV files found in the specified data path.")
            return

        logging.info(f"Found {len(all_files)} CSV files. Loading data...")
        combined_data = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

        # Preprocess data
        logging.info("Preprocessing data...")
        required_features = ['time', 'press_duration', 'inter_key_interval']
        missing_features = [feature for feature in required_features if feature not in combined_data.columns]
        if missing_features:
            logging.error(f"Missing required features in the data: {missing_features}")
            return

        data_features = combined_data[required_features].fillna(0)  # Replace NaN with 0

        # Load existing scaler if available
        if os.path.exists(scaler_path):
            logging.info("Existing scaler found. Loading scaler...")
            scaler = joblib.load(scaler_path)
        else:
            logging.info("No existing scaler found. Creating a new one...")
            scaler = StandardScaler()

        # Scale the data
        scaled_data = scaler.fit_transform(data_features)

        # Load existing model if available
        if os.path.exists(model_path):
            logging.info("Existing model found. Loading model...")
            model = joblib.load(model_path)
        else:
            logging.info("No existing model found. Creating a new one...")
            model = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)

        # Train (or continue training) the model
        logging.info("Training One-Class SVM model...")
        model.fit(scaled_data)

        # Save the updated model and scaler
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)

        logging.info(f"Model saved to {model_path}")
        logging.info(f"Scaler saved to {scaler_path}")

    except Exception as e:
        logging.error(f"An error occurred during training or updating: {e}")