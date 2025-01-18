# Abnormal-Activity-Monitoring-System

Here's a polished and simplified version of the PDF content rewritten as a `README.md` file suitable for GitHub:

---

# Abnormal Activity Monitoring System

This project monitors and detects anomalies in file access, keyboard inputs, mouse movements, and IP changes in real time. It features an interactive web interface built with Streamlit and uses machine learning models to analyze and respond to unusual system behavior.

---

## Features

### Core Components
1. **MongoDB Integration**  
   - Logs are stored in collections for various activities: `File_abnormalities`, `Keyboard_abnormalities`, `Mouse_abnormalities`, and `IP_abnormalities`.

2. **Streamlit Web Application**  
   - Provides navigation via a sidebar for:  
     - **Dashboard**: Displays system metrics and visualizations.  
     - **Instructions**: Guides for initializing and using the monitoring system.  
     - **Utilities**: Tools to clean directories and maintain the system.  

3. **Visualization Tools**  
   - Real-time insights via bar charts, line charts, histograms, and heatmaps using **Plotly**, **Seaborn**, and **Matplotlib**.

4. **Machine Learning Models**  
   - **Isolation Forest**: Detects file access anomalies.  
   - **One-Class SVM**: Analyzes keyboard usage patterns.  
   - **Autoencoder**: Identifies irregular mouse movements.  
   - **Random Forest**: Tracks unusual IP changes.

5. **Multi-threaded Execution**  
   - Enables concurrent monitoring scripts for file, keyboard, mouse, and IP logs.

---

## System Workflow

### 1. Monitoring Process
- **Directory Setup**:  
  The `Records` directory contains subdirectories for logs:
  - `file_access_log`, `key_log`, `mouse_data_log`, `ip_change_log`.

- **Real-Time Monitoring Scripts**:  
  - `FI_R.py`: Logs file access events.  
  - `KI_R.py`: Tracks keyboard activity.  
  - `MI_R.py`: Monitors mouse movements.  
  - `IPI_R.py`: Observes IP address changes.

- **Graceful Termination**:  
  Monitoring scripts can be stopped by pressing the `Esc` key.

### 2. Training Process
Run the `Train.py` script to train four ML models:
- Models process logs collected over a **7-day period**.  
- Outputs are stored in the `Models` directory.  

---

## How to Run the Application

### Prerequisites
1. **Install Dependencies**:  
   Install the required Python libraries:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Connect MongoDB**:  
   Ensure MongoDB is running and accessible.

### Steps to Execute
1. **Run the Streamlit App**:  
   ```bash
   streamlit run app.py
   ```

2. **Clear Previous Logs** (if needed):  
   Use the "Utilities" section in the app or manually delete files in the `Models` and `Records` directories.

3. **Start Monitoring**:  
   Run the monitoring script to collect logs:  
   ```bash
   python Monitor.py
   ```

4. **Train the Models**:  
   Process the collected logs and train the models:  
   ```bash
   python Train.py
   ```

---

## Key Functionalities

### Machine Learning Models
1. **Isolation Forest**  
   - Identifies file access anomalies by training on normal behaviors.  

2. **One-Class SVM**  
   - Detects unusual keyboard activity patterns.  

3. **Autoencoder**  
   - Recognizes irregular mouse movements using reconstruction errors.  

4. **Random Forest**  
   - Analyzes IP changes for abnormal transitions.

### Utilities
- Scripts for clearing old logs:  
  - `Clean_Models.py`: Deletes model files.  
  - `Clean_Records.py`: Clears log files.

### Visualizations
- **File Access Patterns**: Bar charts for event types.  
- **IP Change Trends**: Line charts for packet flow over time.  
- **Keyboard Patterns**: Histograms for inter-key intervals and line charts for key press durations.  
- **Mouse Movements**: Heatmaps for density and trends in speed.

---

## Enhancements and Future Improvements
- **Error Handling**: Add detailed logs for subprocess issues.  
- **Dynamic Parameters**: Allow users to configure thresholds and model settings.  
- **Real-Time Integration**: Enable live anomaly detection based on incoming logs.  
- **Visualization**: Include more interactive charts to explore anomalies.

---

## Use Cases
- **Security Monitoring**: Detect unauthorized activities in real time.  
- **Behavioral Analysis**: Analyze user interaction patterns.  
- **Proactive Detection**: Identify issues before they escalate.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

Let me know if you'd like any further adjustments!