import joblib
import tensorflow as tf
import numpy as np
import pandas as pd


# Prediction using the Random Forest Classifier for IP Change Logs
def predict_ip_change(ip_change_data, model_path="Models/ip_change_log/ip_anomaly_detector.pkl"):
    """
    Predict anomalies in IP change logs using the Random Forest Classifier.

    :param ip_change_data: DataFrame containing IP change data with required features.
    :param model_path: Path to the saved Random Forest model.
    :return: A list of human-readable predictions.
    """
    model = joblib.load(model_path)
    predictions = model.predict(ip_change_data)
    readable_predictions = ["Normal" if pred == 1 else "Anomalous" for pred in predictions]
    return readable_predictions


# Prediction using the Isolation Forest Pipeline for File Access Logs
def predict_file_access(file_access_data,
                        model_path="Models/file_access_log/file_access_isolation_forest_pipeline.pkl"):
    """
    Predict anomalies in file access logs using the Isolation Forest pipeline.

    :param file_access_data: DataFrame containing file access data with required features.
    :param model_path: Path to the saved Isolation Forest pipeline.
    :return: A list of human-readable predictions.
    """
    pipeline = joblib.load(model_path)
    predictions = pipeline.predict(file_access_data)
    readable_predictions = ["Normal" if pred == 1 else "Anomalous" for pred in predictions]
    return readable_predictions


# Prediction using the One-Class SVM for Key Logs
def predict_key_log(key_log_data, scaler_path="Models/key_log/key_scaler.pkl",
                    model_path="Models/key_log/key_svm_model.pkl"):
    """
    Predict anomalies in key logs using One-Class SVM.

    :param key_log_data: DataFrame containing key log data with required features.
    :param scaler_path: Path to the saved scaler.
    :param model_path: Path to the saved One-Class SVM model.
    :return: A list of human-readable predictions.
    """
    scaler = joblib.load(scaler_path)
    model = joblib.load(model_path)
    scaled_data = scaler.transform(key_log_data)
    predictions = model.predict(scaled_data)
    readable_predictions = ["Normal" if pred == 1 else "Anomalous" for pred in predictions]
    return readable_predictions


# Prediction using the Autoencoder for Mouse Data Logs
def predict_mouse_data(mouse_data, autoencoder_path="Models/mouse_data_log/mouse_autoencoder.keras",
                       preprocessor_path="Models/mouse_data_log/mouse_preprocessor.pkl", threshold=0.5):
    """
    Predict reconstruction errors in mouse data logs using an autoencoder.

    :param mouse_data: DataFrame containing mouse data with required features.
    :param autoencoder_path: Path to the saved autoencoder model.
    :param preprocessor_path: Path to the saved preprocessor.
    :param threshold: Error threshold above which data is considered anomalous.
    :return: A list of human-readable predictions.
    """
    preprocessor = joblib.load(preprocessor_path)
    autoencoder = tf.keras.models.load_model(autoencoder_path)
    processed_data = preprocessor.transform(mouse_data)
    reconstructed = autoencoder.predict(processed_data)
    reconstruction_error = np.mean((processed_data - reconstructed) ** 2, axis=1)
    readable_predictions = ["Normal" if error <= threshold else "Anomalous" for error in reconstruction_error]
    return readable_predictions


if __name__ == "__main__":
    # Example Usage
    # Load test data for IP change logs
    test_ip_data = pd.read_csv("test_ip_change_log.csv")

    # Preprocess the test data if necessary
    # For demonstration, assuming the test data is already preprocessed

    # Predict IP anomalies
    ip_predictions = predict_ip_change(test_ip_data)
    print("IP Change Log Predictions:", ip_predictions)

    # Similar usage for other log types (file access, key logs, mouse data)
