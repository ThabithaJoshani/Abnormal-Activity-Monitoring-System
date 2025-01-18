import os
import glob
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def load_logs(path):
    """
    Load all CSV files containing IP change logs into a single DataFrame.
    """
    files = glob.glob(path)
    if not files:
        raise FileNotFoundError("No CSV files found in the specified directory.")

    data_frames = [pd.read_csv(file) for file in files]
    return pd.concat(data_frames, ignore_index=True)


def generate_labels(df):
    """
    Generate labels for the dataset based on custom criteria.
    """
    df['label'] = (df['subnet_changed'] == 1).astype(int)  # Example: subnet changes as anomalies
    return df


def preprocess_logs(df):
    """
    Preprocess the logs by engineering relevant features.
    """
    if df.empty:
        raise ValueError("The input DataFrame is empty.")

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.sort_values(by='timestamp', inplace=True)

    # Drop rows with invalid timestamps
    df = df.dropna(subset=['timestamp'])

    # Time differences between IP changes
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds()

    # IP subnet change detection (first three octets of IP)
    df['subnet'] = df['ip_address'].str.rsplit('.', n=1).str[0]

    # Subnet change flag
    df['subnet_changed'] = (df['subnet'] != df['subnet'].shift()).astype(int)

    # Encode event_type
    df['event_type_encoded'] = df['event_type'].map({'initial_ip': 0, 'ip_changed': 1})

    # Drop unnecessary columns
    columns_to_drop = ['timestamp', 'ip_address', 'subnet', 'host_name', 'event_type']
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

    # Handle missing values
    df.fillna(0, inplace=True)

    # Generate labels
    df = generate_labels(df)

    return df


def train_or_update_random_forest(data, save_path):
    """
    Train or update a Random Forest Classifier for IP change anomaly detection and save the model.
    """
    if data.empty:
        raise ValueError("The dataset is empty. Cannot train the model.")

    if 'label' not in data.columns:
        raise ValueError("The dataset must contain a 'label' column for supervised training.")

    X = data.drop(columns=['label'])
    y = data['label']

    # Check if the dataset has enough samples for train-test split
    if len(data) > 1:
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    else:
        # Use all data for training if samples are insufficient
        X_train, y_train = X, y
        X_test, y_test = X, y

    model_path = os.path.join(save_path, "ip_anomaly_detector.pkl")

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

    try:
        logs = load_logs(LOG_FILES_PATH)
        data = preprocess_logs(logs)
        train_or_update_random_forest(data, MODELS_DIR)
    except Exception as e:
        print(f"Error: {e}")
