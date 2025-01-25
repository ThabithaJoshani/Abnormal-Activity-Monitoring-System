import logging
import os
import joblib
import pandas as pd
from keras import Input, Model
from keras.src.saving import load_model
from keras.src.layers import Dense, BatchNormalization, Dropout
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def train_or_update_autoencoder(data_path, save_path):
    """
    Train or update an autoencoder model for anomaly detection in mouse data logs.

    :param data_path: Path to the directory containing CSV files.
    :param save_path: Path to save or load the trained model and preprocessing pipeline.
    """
    try:
        # Ensure save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Define file paths
        autoencoder_path = os.path.join(save_path, "mouse_autoencoder.keras")
        preprocessor_path = os.path.join(save_path, "mouse_preprocessor.pkl")

        # Read and combine all CSV files
        logging.info("Collecting CSV files...")
        all_files = [os.path.join(data_path, file) for file in os.listdir(data_path) if file.endswith('.csv')]
        if not all_files:
            logging.error("No CSV files found in the specified data path.")
            return

        logging.info(f"Found {len(all_files)} CSV files. Loading data...")
        combined_data = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

        # Preprocess data: Drop session_id and handle missing values
        if 'session_id' in combined_data.columns:
            combined_data = combined_data.drop(columns=['session_id'])
        combined_data = combined_data.fillna(0)  # Fill missing values with 0

        # Ensure categorical columns are strings
        if 'button' in combined_data.columns:
            combined_data['button'] = combined_data['button'].astype(str)
        if 'scroll' in combined_data.columns:
            combined_data['scroll'] = combined_data['scroll'].astype(str)

        # Features for training
        features = ['x', 'y', 'speed', 'button', 'time', 'scroll']

        missing_features = [feature for feature in features if feature not in combined_data.columns]
        if missing_features:
            logging.error(f"Missing required features: {missing_features}")
            return

        # Preprocessing: Standardize numerical features and encode categorical features
        numerical_features = ['x', 'y', 'speed', 'time']
        categorical_features = ['button', 'scroll']

        numerical_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )

        logging.info("Preprocessing data...")
        processed_data = preprocessor.fit_transform(combined_data)

        # Load existing model or define a new one
        if os.path.exists(autoencoder_path) and os.path.exists(preprocessor_path):
            logging.info("Existing model found. Loading model and preprocessor...")
            autoencoder = load_model(autoencoder_path)
            preprocessor = joblib.load(preprocessor_path)
            logging.info("Model and preprocessor loaded successfully.")
        else:
            logging.info("No existing model found. Creating a new model...")
            # Define Autoencoder model
            input_dim = processed_data.shape[1]
            encoding_dim = max(2, input_dim // 2)  # Ensure encoding dimension is at least 2

            input_layer = Input(shape=(input_dim,))
            encoder = Dense(encoding_dim, activation="relu")(input_layer)
            encoder = BatchNormalization()(encoder)
            encoder = Dropout(0.2)(encoder)

            decoder = Dense(input_dim, activation="sigmoid")(encoder)
            autoencoder = Model(inputs=input_layer, outputs=decoder)
            autoencoder.compile(optimizer="adam", loss="mse")

        # Train (or continue training) the model
        logging.info("Training autoencoder model...")
        autoencoder.fit(
            processed_data, processed_data,
            epochs=50, batch_size=32, shuffle=True, verbose=1
        )

        # Save the model and preprocessor
        autoencoder.save(autoencoder_path)
        joblib.dump(preprocessor, preprocessor_path)

        logging.info(f"Autoencoder model saved to {autoencoder_path}")
        logging.info(f"Preprocessor saved to {preprocessor_path}")

    except Exception as e:
        logging.error(f"An error occurred during training: {e}")
