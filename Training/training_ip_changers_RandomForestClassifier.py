import pandas as pd
import glob
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def load_logs(path):
    """
    Load all CSV files containing IP change logs into a single DataFrame.

    :param path: Path to the log files.
    :return: Combined DataFrame.
    """
    files = glob.glob(path)
    data_frames = [pd.read_csv(file) for file in files]
    return pd.concat(data_frames, ignore_index=True)


def preprocess_logs(df):
    """
    Preprocess the logs by engineering relevant features.

    :param df: Raw DataFrame containing the logs.
    :return: Preprocessed DataFrame with features ready for training.
    """
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)

    # Time differences between IP changes
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds()

    # IP subnet change detection (first three octets of IP)
    df['subnet'] = df['ip_address'].str.rsplit('.', 1).str[0]

    # Subnet change flag
    df['subnet_changed'] = (df['subnet'] != df['subnet'].shift()).astype(int)

    # Encode event_type
    df['event_type_encoded'] = df['event_type'].map({'initial_ip': 0, 'ip_changed': 1})

    # Drop unnecessary columns
    df.drop(columns=['timestamp', 'ip_address', 'subnet', 'host_name', 'event_type'], inplace=True)

    # Handle missing values
    df.fillna(0, inplace=True)

    return df


def train_or_update_random_forest(data_path, save_path):
    """
    Train or update a Random Forest Classifier for IP change anomaly detection and save the model.

    :param data_path: Path to the directory containing CSV files.
    :param save_path: Path to save or load the trained model.
    """
    # Load logs
    logs = load_logs(data_path)

    # Preprocess logs
    data = preprocess_logs(logs)

    # Generate labels (For demonstration, replace this with actual labeling logic)
    # Assuming the last column 'label' is pre-added in the data for supervised training
    if 'label' not in data.columns:
        raise ValueError("The dataset must contain a 'label' column for supervised training.")

    X = data.drop(columns=['label'])
    y = data['label']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model_path = f"{save_path}/ip_anomaly_detector.pkl"

    try:
        # Load existing model if available
        if os.path.exists(model_path):
            print("Loading existing Random Forest model...")
            model = joblib.load(model_path)
        else:
            print("No existing model found. Creating a new Random Forest model...")
            model = RandomForestClassifier(random_state=42)

        # Train the model
        print("Training Random Forest model...")
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Save the trained model
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")

    except Exception as e:
        print(f"Error during training or updating the model: {e}")


if __name__ == "__main__":
    LOG_FILES_PATH = "./Records/ip_change_log/*.csv"
    MODELS_DIR = "Models/ip_change_log"

    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

    train_or_update_random_forest(LOG_FILES_PATH, MODELS_DIR)
