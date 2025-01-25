from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd
import os
import logging


def train_or_update_isolation_forest(data_path, save_path):
    """
    Train or update an Isolation Forest model on file access logs.

    :param data_path: Path to the directory containing CSV files.
    :param save_path: Directory to save or load the trained model and preprocessing pipeline.
    """
    try:
        # Ensure save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Define file path for the pipeline
        pipeline_path = os.path.join(save_path, "file_access_isolation_forest_pipeline.pkl")

        # Collect and combine all CSV files in the data_path directory
        if not os.path.isdir(data_path):
            logging.error(f"{data_path} is not a valid directory.")
            return

        logging.info(f"Collecting CSV files from {data_path}...")
        all_files = [os.path.join(data_path, file) for file in os.listdir(data_path) if file.endswith('.csv')]
        if not all_files:
            logging.error(f"No CSV files found in {data_path}.")
            return

        logging.info(f"Found {len(all_files)} CSV files. Loading data...")
        data = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

        # Preprocess data: Drop irrelevant columns and handle data types
        if 'hash' in data.columns:
            data = data.drop(columns=['hash'])
        if 'is_directory' in data.columns:
            data['is_directory'] = data['is_directory'].astype(int)  # Convert bool to int

        # Define features for training
        features = ['event_type', 'file_path', 'time', 'is_directory']

        # Ensure required features are present
        missing_features = [feature for feature in features if feature not in data.columns]
        if missing_features:
            logging.error(f"Missing required features in the data: {missing_features}")
            return

        # Define preprocessing steps
        numerical_features = ['time', 'is_directory']
        categorical_features = ['event_type', 'file_path']

        numerical_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )

        # Load existing pipeline if available, otherwise create a new one
        if os.path.exists(pipeline_path):
            logging.info("Existing pipeline found. Loading pipeline...")
            pipeline = joblib.load(pipeline_path)
            logging.info("Pipeline loaded successfully.")
        else:
            logging.info("No existing pipeline found. Creating a new one...")
            model = IsolationForest(contamination=0.01, random_state=42)
            pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])

        # Train (or continue training) the model
        logging.info("Training Isolation Forest...")
        pipeline.fit(data[features])

        # Save the updated pipeline
        joblib.dump(pipeline, pipeline_path)
        logging.info(f"Pipeline saved to {pipeline_path}.")

    except Exception as e:
        logging.error(f"Error in train_or_update_isolation_forest: {e}")

