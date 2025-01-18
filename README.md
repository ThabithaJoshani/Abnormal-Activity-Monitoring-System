# Abnormal-Activity-Monitoring-System


Note – please connect the MongoDB before that ting all
App running – app.py
Code – Streamlit run app.py
Key Components of the Code
1.
MongoDB Setup:
o
MongoDB is connected using the pymongo library.
o
Collections (File_abnormalities, Keyboard_abnormalities, Mouse_abnormalities, and IP_abnormalities) store specific types of abnormal activity logs.
2.
Utility Function:
o
fetch_data: Retrieves data from MongoDB collections with an optional limit parameter to cap the number of records.
3.
Streamlit Setup:
o
Streamlit is used to build the web app interface with various sections accessible via a sidebar menu (Dashboard, Instructions, Utilities, etc.).
o
Custom CSS styles are added for branding and to create visual effects like a blinking alert box.
4.
Sidebar Navigation:
o
A radio widget in the sidebar enables users to switch between sections:
▪
Dashboard: Displays metrics and an overview of abnormalities.
▪
Instructions: Guides users on running the monitoring system.
▪
Utilities: Provides buttons to clear model and record directories.
5.
Instructions Section:
o
Provides detailed steps for initializing the anomaly monitoring process, including manually running scripts (Monitor.py and Train.py) and configuring the system.
6.
Utilities Section:
o
Allows cleaning directories (e.g., Models and Records) using external Python scripts (Clean_Models.py and Clean_Records.py).
o
Executes the scripts using the subprocess module, capturing the output and showing success/error messages.
7.
Dashboard Section:
o
Fetches and displays real-time metrics from MongoDB collections, including counts of abnormal file events, IP changes, keyboard events, and mouse events.
8.
Specific Patterns Sections:
o
File Access Patterns:
▪
Displays data from the File_abnormalities collection.
▪
Visualizes event types distribution using a bar chart.
o
IP Changing Patterns:
▪
Simulates or fetches IP-related abnormality data.
▪
Plots events over time and packet flow using line charts.
o
Keyboard Patterns:
▪
Shows inter-key interval distribution (histogram).
▪
Trends of key press duration (line chart).
▪
Correlation heatmap between inter-key interval and press duration.
o
Mouse Patterns:
▪
Displays mouse speed trends.
▪
Generates a heatmap for mouse movement using sns.kdeplot to show movement density.
9.
Visualizations:
o
Plotly:
▪
Used for interactive visualizations like bar charts, line charts, and histograms.
o
Seaborn & Matplotlib:
▪
Used for static visualizations like correlation heatmaps and mouse movement density plots.
10.
Footer:
o
Adds a footer for branding and copyright details.
How the Code Works:
1.
Data Collection:
o
The monitoring system collects abnormality data for file access, keyboard input, mouse movements, and IP changes and stores it in MongoDB.
2.
Interactive Navigation:
o
The sidebar allows users to select sections like the dashboard, instructions, utilities, or specific pattern analysis.
3.
Real-time Metrics:
o
Key statistics (e.g., counts of abnormalities) are displayed in the dashboard using Streamlit's metric widget.
4.
Detailed Visualizations:
o
Each section provides interactive and visual insights into specific types of anomalies using appropriate charts.
5.
Utilities for Maintenance:
o
Users can clear directories for models and records to ensure the system operates efficiently.
Purpose of the Application:
The Abnormal Activity Monitoring System is designed to provide:
•
Real-time monitoring of system behaviors.
•
Interactive insights into anomalies using visualization tools.
•
A user-friendly interface for both technical and non-technical users to analyze and act on anomalies.
This system can be extended for:
•
Security monitoring in IT environments.
•
Behavioral analysis for user and system interactions.
•
Log analysis for proactive anomaly detection and response.
Interface will display.
Please read the instructions – In here we have to clear models and records directories since earlier works should be happening.
After clearing the directories, we have to run, 1. Monitor.py (Gathering 4 logs such as File access, IP changing, Key logs, Mouse pattern)
Functionality Overview
1.
Directory Setup:
o
The Records directory is created, with subdirectories for different types of logs (file_access_log, key_log, mouse_data_log, and ip_change_log).
2.
Script Execution:
o
Each monitoring script is executed in its own thread, allowing them to run concurrently.
o
The script paths are specified in the SCRIPT_PATHS list.
3.
Stopping Mechanism:
o
A global flag, stop_all_scripts, is used to signal all threads to stop execution.
o
A keyboard listener monitors for the Esc key. When pressed, the stop_all_scripts flag is set to True, which terminates all running scripts.
4.
Graceful Termination:
o
Each thread periodically checks the stop_all_scripts flag. When set to True, it terminates the corresponding subprocess running the script.
5.
Thread Management:
o
The threading module is used to create and manage threads. The daemon property ensures that threads do not block the program from exiting.
Key Components
Directory Setup
• Ensures the directory structure exists before running the monitoring scripts.
• The structure is used to store logs generated by the monitoring scripts.
Running Monitoring Scripts
• Each script is executed using subprocess.Popen.
• The thread running this function checks the stop_all_scripts flag every second. If set, it terminates the subprocess.
Listening for Esc Key
• Uses pynput.keyboard.Listener to detect keypress events.
• If the Esc key is pressed, sets the stop_all_scripts flag to True.
Main Execution
•
Initializes and starts a thread for each monitoring script.
•
Starts another thread for the keyboard listener to detect the Esc key.
•
Ensures all threads run concurrently, and the main program waits for them to finish using join.
Use Case
•
This script is ideal for scenarios where multiple monitoring processes need to run simultaneously, such as:
o
Logging file access.
o
Monitoring keyboard or mouse activity.
o
Detecting IP address changes.
•
The keyboard listener provides an intuitive way to terminate all processes.
Key Benefits
1.
Concurrent Execution:
o
Multiple scripts run independently without blocking each other.
2.
Graceful Shutdown:
o
Ensures all subprocesses terminate when the Esc key is pressed or the program is interrupted.
3.
Extensibility:
o
Additional scripts can be added to SCRIPT_PATHS without modifying the core logic.
Enhancements
1.
Error Handling:
o
Add logging for errors to troubleshoot subprocess execution issues.
2.
Dynamic Script Paths:
o
Allow users to specify script paths via a configuration file or command-line arguments.
3.
Health Monitoring:
o
Add periodic health checks for subprocesses to ensure they are running as expected.
Generally, we have to run this process for 7 days to collect the logs for train the models.
If not, you can stop the monitoring process by pressing “Esc” button.
Inside the monitoring process, we are using 4 collectors. 1. FI_R.py – Collecting file access logs
Key Features
1.
Real-Time Monitoring:
o
Uses watchdog to detect file system events in real-time.
o
Monitors changes like file creation, deletion, modification, and movement.
2.
Logging to CSV:
o
Logs events into a CSV file with details such as event type, file path, timestamp, whether it's a directory, and file hash.
3.
File Integrity Check:
o
Generates an MD5 hash for files to track and detect duplicates or changes in content.
4.
Escape Key Listener:
o
Uses pynput to listen for the Esc key, allowing the user to gracefully stop the monitoring process.
5.
Threaded Execution:
o
Runs file monitoring in a separate thread to keep the main program responsive and ready to handle user input.
Detailed Explanation
1. Log File Setup
• Creates a uniquely named log file based on the current timestamp.
• Ensures logs are organized and easily traceable.
2. CSV File Initialization
•
If the log file does not exist, it's created with predefined column headers.
3. File Hash Calculation
•
Calculates the MD5 hash of a file to track content changes.
•
Helps detect duplicate or altered files.
4. File System Event Handling
•
Handles different file system events (created, deleted, modified, moved).
•
Logs details of each event, including:
o
Event type (created, deleted, etc.)
o
File path
o
Timestamp
o
Whether it's a directory
o
File hash (if applicable)
5. Ignore Excluded Paths
•
Skips logging for paths under the excluded directory (./Records) to avoid recursive logging of the log file itself.
6. File Monitoring
•
Sets up a watchdog.Observer to monitor the specified directory and its subdirectories recursively.
7. Keyboard Listener for Stopping
•
Listens for the Esc key to set the stop_logging flag, signaling the program to stop.
8. Multithreading
Runs the file monitoring in a separate thread to keep the main thread available for user input.
2.IPI_R.py – Collecting IP logs
Core Features
1.
Public IP Monitoring:
o
Periodically checks the current public IP address using the https://api.ipify.org API.
o
Detects and logs changes in the public IP address.
2.
Logging:
o
Logs events such as the initial IP address and subsequent IP changes into a timestamped CSV file.
o
Logs include the event type (initial_ip, ip_changed), timestamp, IP address, and the device's hostname.
3.
Keyboard Listener:
o
Listens for the Esc key to stop monitoring gracefully.
4.
Threaded Execution:
o
Runs the IP monitoring in a background thread to keep the main program responsive and ready to handle user input.
3.KI_R.py – Collecting Key Logs
Core Features
1.
Key Logging:
o
Captures key presses and releases, logging each event along with associated metadata:
▪
Key: The character or key pressed.
▪
Event: Whether it’s a key press or release.
▪
Time: Timestamp of the event.
▪
Press Duration: Time between a key press and its release.
▪
Release Time: Exact time when the key was released.
▪
Inter-Key Interval: Time elapsed between the release of the last key and the press of the current key.
▪
Session ID: Unique identifier for the logging session.
2.
Logging to CSV:
o
Logs keystroke data into a CSV file, ensuring persistent storage.
o
Logs are saved in batches for efficiency, and any remaining logs are saved before exiting.
3.
Escape Key Listener:
o
Allows the user to stop the logger gracefully by pressing the Esc key.
4.
Threading:
o
Runs the keyboard listener in a background thread, keeping the main thread responsive.
3.MI_R.py – Collecting mouse moves
Core Features
1.
Mouse Event Logging:
o
Tracks mouse movements, clicks, and scroll events.
o
Logs details such as:
▪
Event Type: move, click_press, click_release, or scroll.
▪
Coordinates: x and y positions of the mouse.
▪
Speed: Calculated movement speed (distance/time).
▪
Button: Details of the mouse button involved in clicks.
▪
Scroll: Scroll direction and amount.
2.
Session Logging:
o
Each session has a unique ID (session_id) based on the current timestamp.
o
Logs are saved in a CSV file for persistent storage.
3.
Keyboard Listener:
o
Monitors for the Esc key to stop logging gracefully.
4.
Threaded Execution:
o
Uses separate threads for mouse and keyboard listeners to run concurrently without blocking each other.
Stope the running of Monitor.py Process.
2.Next We have to run Train.py file for train the 4 models for 4 anomalies.
Core Features
1.
Directory and File Processing:
o
Scans predefined directories (file_access_log, key_log, mouse_data_log, ip_change_log) for CSV files.
o
Processes log files using specialized training functions for each log type.
2.
Model Training:
o
Each type of log has a corresponding machine learning model:
▪
Isolation Forest for file access logs.
▪
One-Class SVM for keyboard logs.
▪
Autoencoder for mouse data logs.
▪
Random Forest for IP change logs.
3.
Model Storage:
o
Saves trained models in a centralized Models directory, organized by log type.
4.
File Management:
o
Moves processed log files into a trained subdirectory to avoid reprocessing.
5.
Database Update:
o
Runs database.py to update a MongoDB database with the latest results.
In here using 4 ML models for training the 4 models 1.Isolation Forest for file access logs.
Key Features
1.
Data Collection:
o
Collects and combines all CSV files from the specified directory (data_path).
2.
Preprocessing:
o
Drops irrelevant columns (e.g., hash) and handles missing or invalid values.
o
Uses StandardScaler for numerical features and OneHotEncoder for categorical features to standardize and encode data.
3.
Isolation Forest Training:
o
Trains an Isolation Forest model for anomaly detection.
o
Uses contamination=0.01 to specify the proportion of anomalies in the data.
4.
Pipeline Management:
o
Saves the preprocessing and model pipeline to a file (file_access_isolation_forest_pipeline.pkl) for reuse.
o
Reloads and updates an existing pipeline if available.
5.
Logging:
o
Provides detailed logging for debugging and tracking the training process.
Detailed Explanation
1. Pipeline Management
•
Specifies the file path for saving the preprocessing pipeline and trained model.
•
If a pipeline already exists, it is loaded for reuse to avoid retraining from scratch.
2. Data Collection
•
Collects all CSV files from the data_path directory and loads them into a single Pandas DataFrame.
•
Ensures efficient handling of multiple log files.
3. Preprocessing
•
Numerical Features:
o
Scales time and is_directory using StandardScaler to normalize the data.
•
Categorical Features:
o
Encodes event_type and file_path using OneHotEncoder.
•
ColumnTransformer:
o
Combines preprocessing steps for numerical and categorical features.
4. Model Training
•
The Isolation Forest:
o
Detects anomalies in the preprocessed data.
o
contamination=0.01 assumes 1% of the data are anomalies.
•
The Pipeline:
o
Combines preprocessing and the Isolation Forest model into a single reusable structure.
5. Saving and Loading the Pipeline
•
Saving:
o
Stores the trained pipeline for future use.
•
Loading:
o
Reloads an existing pipeline to continue training or to apply the model to new data.
6. Error Handling
•
Validates the input directory and ensures that it contains CSV files.
•
Logs any errors during training or preprocessing.
Execution Flow
1.
Input:
o
Takes the data_path (directory containing log files) and save_path (directory for saving the model pipeline).
2.
Preprocessing:
o
Reads and preprocesses data from the log files.
3.
Model Training:
o
Trains or updates an Isolation Forest model.
4.
Save Pipeline:
o
Saves the pipeline to a file for future use.
Usage Example
Use Cases
1.
Anomaly Detection:
o
Identify unusual patterns in file access logs.
2.
Automated Model Updating:
o
Update the model incrementally as new data becomes available.
3.
Log Analysis:
o
Analyze historical log data to improve system security.
Possible Enhancements
1.
Dynamic Contamination Parameter:
o
Allow the user to specify the contamination ratio.
2.
Error Handling:
o
Add more detailed error messages and recovery options.
3.
Visualization:
o
Include visualizations of anomalies detected during training.
4.
Batch Processing:
o
Process logs in batches to handle large datasets efficiently.
2.One-Class SVM for keyboard logs.
Key Features
1.
Data Collection:
o
Combines all CSV files in the specified directory into a single dataset.
2.
Preprocessing:
o
Extracts relevant features: time, press_duration, and inter_key_interval.
o
Handles missing values by replacing NaN with 0.
3.
Model Training:
o
Trains a One-Class SVM with a radial basis function (RBF) kernel.
o
Suitable for detecting anomalies in a one-class dataset (e.g., normal keyboard activity).
4.
Model Persistence:
o
Saves the trained model and the preprocessing scaler using joblib.
5.
Logging:
o
Provides detailed logs for every step of the process to aid debugging and transparency.
Detailed Explanation
1. Setup for Model and Scaler
•
Specifies file paths for saving the trained model and the scaler.
•
Ensures that these artifacts can be reused in subsequent runs.
2. Data Collection
•
Searches for all CSV files in the given directory.
•
Combines data from multiple files into a single Pandas DataFrame.
3. Preprocessing
•
Ensures that the required features (time, press_duration, inter_key_interval) are present in the dataset.
•
Replaces missing values (NaN) with 0 for robustness.
4. Scaler Management
•
Loads an existing StandardScaler if available, or creates a new one.
•
Scales the data to ensure consistent input for the SVM model.
5. Model Training
•
Loads an existing model if available, or initializes a new One-Class SVM with the following parameters:
o
kernel='rbf': Radial basis function kernel for non-linear decision boundaries.
o
gamma='scale': Scales the kernel coefficient based on the data.
o
nu=0.05: Specifies the proportion of data to consider as anomalies.
6. Saving Model and Scaler
•
Saves the trained model and the scaler to ensure they can be reused without retraining.
Execution Flow
1.
Directory and File Validation:
o
Ensures the data_path directory exists and contains CSV files.
2.
Data Loading and Preprocessing:
o
Combines log files and preprocesses data to extract required features.
3.
Scaler and Model Management:
o
Loads existing artifacts or initializes new ones.
4.
Model Training:
o
Trains the One-Class SVM on the preprocessed data.
5.
Saving Artifacts:
o
Saves the trained model and scaler for future use.
Use Cases
•
Keyboard Anomaly Detection:
o
Identify unusual keyboard usage patterns (e.g., unauthorized activity or erratic behavior).
•
Behavior Analysis:
o
Analyze typing habits to identify deviations from normal behavior.
Possible Enhancements
1.
Dynamic Parameters:
o
Allow customization of nu (contamination level) and gamma (kernel coefficient) via user input or a configuration file.
2.
Visualization:
o
Provide visual feedback on the training results, such as a plot of anomaly scores.
3.
Batch Processing:
o
Handle large datasets by processing them in smaller batches to reduce memory usage.
4.
Real-Time Integration:
o
Use the trained model for real-time anomaly detection on live keyboard events.
3.Autoencoder for mouse data logs.
Key Features
1.
Data Collection:
o
Combines multiple CSV files from the specified directory into a single dataset.
2.
Data Preprocessing:
o
Numerical features are standardized using StandardScaler.
o
Categorical features are encoded using OneHotEncoder.
o
Handles missing values and ensures correct data types.
3.
Autoencoder Model:
o
A neural network designed to reconstruct its input.
o
Learns patterns of normal behavior, making it suitable for anomaly detection.
4.
Model Persistence:
o
Saves the trained autoencoder and preprocessing pipeline for reuse.
5.
Logging:
o
Provides detailed logs for monitoring progress and debugging.
Detailed Explanation
1. Setup for Model and Preprocessor
•
Specifies paths for saving the trained autoencoder model and the preprocessing pipeline.
•
Ensures these files are reusable for future predictions or updates.
2. Data Collection
•
Searches for CSV files in the specified directory.
•
Combines all files into a single Pandas DataFrame for processing.
3. Preprocessing
Feature Selection
•
StandardScaler: Standardizes numerical features to have zero mean and unit variance.
•
OneHotEncoder: Converts categorical features into binary-encoded columns.
4. Autoencoder Model
New Model Initialization
•
Input Layer: Matches the number of features in the preprocessed data.
•
Encoder: Reduces dimensionality to learn compressed representations.
•
Decoder: Reconstructs the original input from the compressed representation.
•
Loss Function: Mean squared error (mse) measures reconstruction accuracy.
•
Optimizer: Adam optimizer for efficient training.
5. Training
•
Trains the autoencoder for 50 epochs with a batch size of 32.
•
Uses the input data as both input and target to reconstruct the original input.
6. Saving Artifacts
•
Autoencoder: Saved using Keras's save method.
•
Preprocessor: Saved using joblib.
Execution Flow
1.
Data Collection:
o
Combines log files from the specified directory.
2.
Preprocessing:
o
Standardizes numerical features and encodes categorical features.
o
Handles missing values.
3.
Model Management:
o
Loads existing model and preprocessor if available.
o
Creates a new model and preprocessor if not.
4.
Model Training:
o
Trains the autoencoder to reconstruct input data.
5.
Saving Artifacts:
o
Saves the trained model and preprocessing pipeline.
Use Cases
1.
Anomaly Detection:
o
Identify unusual patterns in mouse data logs (e.g., erratic movement).
2.
Behavioral Analysis:
o
Study normal mouse usage patterns for ergonomic or usability research.
3.
Real-Time Monitoring:
o
Detect anomalies in live data streams by comparing reconstruction errors.
Possible Enhancements
1.
Dynamic Parameters:
o
Allow users to configure training parameters (e.g., epochs, batch size) via a configuration file.
2.
Visualization:
o
Plot reconstruction loss to monitor training performance.
3.
Anomaly Threshold:
o
Set a threshold for reconstruction error to classify anomalies.
4.
Real-Time Deployment:
o
Integrate with a system to detect anomalies in real-time mouse activity.
4.Random Forest for IP change logs.
Key Features
1.
Log File Aggregation:
o
Loads multiple CSV files containing IP change logs into a single dataset.
2.
Preprocessing:
o
Converts timestamps to datetime and calculates time differences.
o
Detects subnet changes and encodes them as features.
o
Encodes categorical features like event_type.
o
Handles missing values and drops unnecessary columns.
3.
Label Generation:
o
Creates labels for supervised learning by marking subnet changes as anomalies.
4.
Model Training:
o
Trains a Random Forest Classifier on the processed data.
o
Evaluates the model using a train-test split and prints a classification report.
5.
Model Persistence:
o
Saves the trained model to a specified directory for reuse.
Detailed Explanation
1. Loading Logs
•
Uses glob to find all CSV files matching the specified pattern.
•
Combines them into a single Pandas DataFrame.
2. Preprocessing
Feature Engineering
•
Time Differences: Calculates the time elapsed between consecutive IP changes.
•
Subnet Changes: Identifies changes in the subnet (first three octets of the IP).
•
Event Type Encoding: Encodes event_type as integers for model compatibility.
Handling Missing Values
•
Fills missing values with 0 to ensure the dataset is ready for training.
3. Label Generation
•
Labels subnet changes (subnet_changed == 1) as anomalies (label = 1).
4. Model Training
Train-Test Split
•
Splits the data into training and testing sets (70% train, 30% test).
Model Initialization
•
Initializes a new Random Forest Classifier with default parameters.
Model Evaluation
•
Evaluates the model on the test set using metrics such as precision, recall, and F1-score.
5. Saving the Model
•
Saves the trained model to a file for future use.
Execution Flow
1.
Load Logs:
o
Aggregates CSV files into a single DataFrame.
2.
Preprocess Data:
o
Engineers features, handles missing values, and generates labels.
3.
Train Model:
o
Splits the data, trains the Random Forest Classifier, and evaluates it.
4.
Save Model:
o
Stores the trained model for reuse.
Use Cases
1.
Anomaly Detection:
o
Detect unusual IP changes, such as unauthorized subnet transitions.
2.
Network Security:
o
Identify potential network attacks or misconfigurations.
3.
Log Analysis:
o
Analyze historical IP change logs for patterns and anomalies.
Possible Enhancements
1.
Hyperparameter Tuning:
o
Optimize the Random Forest parameters (e.g., n_estimators, max_depth) using grid search.
2.
Visualization:
o
Plot feature importances to understand which features contribute most to anomaly detection.
3.
Real-Time Monitoring:
o
Integrate the trained model into a live system to detect anomalies in real time.
4.
Error Handling:
o
Add more specific error messages for issues like missing columns or invalid data.
Ater the training process we can see the outputs on application