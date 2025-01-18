import os
import subprocess
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]

# Load collections
file_access_collection = db["File_abnormalities"]
keyboard_collection = db["Keyboard_abnormalities"]
mouse_collection = db["Mouse_abnormalities"]
ip_changing_collection = db["IP_abnormalities"]  # Placeholder for IP Changing


# Utility function to fetch data from MongoDB
def fetch_data(collection, limit=1000):
    return pd.DataFrame(list(collection.find().limit(limit)))


# Centered Title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
    }
    .blinking-alert {
        font-size: 18px;
        font-weight: bold;
        color: white;
        background-color: red;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker {
        50% {
            opacity: 0;
        }
    }
    </style>
    <h1 class="title">Abnormal Activity Monitoring System</h1>
    <div class="blinking-alert">Please read Instructions before starting Anomaly monitoring process</div>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Choose a section:",
    ["Dashboard", "Instructions", "Utilities", "File Access Patterns", "IP Changing Patterns", "Keyboard Patterns",
     "Mouse Patterns"]
)

# Bootstrap integration
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# Instructions Section
if section == "Instructions":
    st.markdown(
        """
        ### Instructions
        At first, you should clear the "Models" and "Records" directories at the **Utilities** tab.

        Next, the step is running the `Monitor.py` file manually.

        In here, if needed, you can adjust "Configuration" settings to collect the monitoring logs by editing configuration settings.

        **Default (Recommended) Configuration Settings**:
        - **Learning Period**: 7 Days
        - **Frequency for Train** (in seconds): 3600
        - **Frequency for Monitoring** (in seconds): 1800

        Now you can run the "Monitoring Process" by running the `Monitor.py` file manually.

        When the monitoring process is completed, please run the `Train.py` file manually.

        At the end of this process, you can review the results in the respective sections.
        """
    )

# Utilities Section
if section == "Utilities":
    st.subheader("Utilities")

    # Button to execute Clean_Models.py
    if st.button("Clean Models Directory"):
        try:
            script_path = os.path.join(os.getcwd(), "Clean_Models.py")
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Models directory cleaned successfully.")
            else:
                st.error(f"Failed to clean Models directory: {result.stderr}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Button to execute Clean_Records.py
    if st.button("Clean Records Directory"):
        try:
            script_path = os.path.join(os.getcwd(), "Clean_Records.py")
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Records directory cleaned successfully.")
            else:
                st.error(f"Failed to clean Records directory: {result.stderr}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Dashboard Section
if section == "Dashboard":
    st.subheader("Overview")
    st.markdown(
        """
        The dashboard provides real-time insights and detailed visualization of detected abnormal activities in 
        File Access, Keyboard Inputs, IP Changing, and Mouse Movements. It offers a comprehensive view of 
        system behavior anomalies through interactive metrics and charts, facilitating proactive monitoring 
        and timely intervention to enhance system security and operational efficiency.
        """
    )

    # Metrics
    file_count = file_access_collection.count_documents({})
    ip_count = ip_changing_collection.count_documents({})
    keyboard_count = keyboard_collection.count_documents({})
    mouse_count = mouse_collection.count_documents({})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Abnormal File Events", file_count)
    col2.metric("Abnormal IP Changes", ip_count)
    col3.metric("Abnormal Keyboard Events", keyboard_count)
    col4.metric("Abnormal Mouse Events", mouse_count)

# File Access Patterns
if section == "File Access Patterns":
    st.subheader("File Access Patterns")
    file_data = fetch_data(file_access_collection)
    if not file_data.empty:
        st.dataframe(file_data)
        st.subheader("File Event Types Distribution")
        event_type_chart = px.bar(file_data, x="event_type", title="Event Types Distribution")
        st.plotly_chart(event_type_chart, use_container_width=True)
    else:
        st.warning("No abnormal file access data available.")


# Function to fetch IP change data from MongoDB (replace with your actual implementation)
def fetch_ip_change_data(limit=100):
    try:
        # Replace this block with actual MongoDB query logic
        # Example data for demonstration purposes
        data = {
            "timestamp": pd.date_range(start="2025-01-01", periods=limit, freq="H"),
            "subnet_changed": [1 if i % 2 == 0 else 0 for i in range(limit)],
            "packet_count": [i * 10 for i in range(limit)],
        }
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error fetching IP change data: {e}")
        return pd.DataFrame()


# Function to display IP Changing Patterns
def display_ip_changing_patterns():
    st.title("IP Changing Patterns")

    # Fetch data
    ip_data = fetch_ip_change_data(limit=100)

    if not ip_data.empty:
        # Convert timestamp to datetime for plotting
        ip_data["timestamp"] = pd.to_datetime(ip_data["timestamp"], errors="coerce")

        # Validate required columns
        if "timestamp" not in ip_data.columns or "subnet_changed" not in ip_data.columns:
            st.error("The data is missing required columns for plotting.")
            return

        # Add a sequential event counter for plotting
        ip_data["event_count"] = range(1, len(ip_data) + 1)

        # Plot IP changing events chart
        st.markdown("### IP Changing Events")
        ip_chart = px.line(
            ip_data,
            x="timestamp",
            y="event_count",
            title="IP Changing Events Over Time",
            labels={"timestamp": "Time", "event_count": "Number of Events"},
            markers=True,
        )
        ip_chart.update_layout(height=300, xaxis_title="Time", yaxis_title="IP Change Count")
        st.plotly_chart(ip_chart, use_container_width=True)

        # Display packet flow chart
        st.markdown("### Packet Flowing Patterns")
        if "packet_count" in ip_data.columns:
            packet_chart = px.line(
                ip_data,
                x="timestamp",
                y="packet_count",
                title="Packet Flowing Over Time",
                labels={"timestamp": "Time", "packet_count": "Packets Count"},
                markers=True,
            )
            packet_chart.update_layout(height=300, xaxis_title="Time", yaxis_title="Packet Count")
            st.plotly_chart(packet_chart, use_container_width=True)
        else:
            st.warning("No packet flowing data available.")
    else:
        st.warning("No IP changing events detected.")


# Add the tab function
if section == "IP Changing Patterns":
    display_ip_changing_patterns()

# Keyboard Patterns
if section == "Keyboard Patterns":
    st.subheader("Keyboard Patterns")

    # Fetch data from MongoDB
    keyboard_data = fetch_data(keyboard_collection)

    if not keyboard_data.empty:
        # Convert time to datetime if available
        if "time" in keyboard_data.columns:
            keyboard_data["time"] = pd.to_datetime(keyboard_data["time"], errors="coerce")

        st.dataframe(keyboard_data)

        # 1. Distribution of Inter-Key Intervals
        st.subheader("Distribution of Inter-Key Intervals")
        if "inter_key_interval" in keyboard_data.columns:
            interval_histogram = px.histogram(
                keyboard_data,
                x="inter_key_interval",
                nbins=30,
                title="Inter-Key Interval Distribution",
                labels={"inter_key_interval": "Inter-Key Interval (ms)"},
            )
            st.plotly_chart(interval_histogram, use_container_width=True)
        else:
            st.warning("'inter_key_interval' column is missing from the data.")

        # 2. Key Press Duration Trends
        st.subheader("Key Press Duration Over Time")
        if "press_duration" in keyboard_data.columns and "time" in keyboard_data.columns:
            press_duration_chart = px.line(
                keyboard_data,
                x="time",
                y="press_duration",
                title="Press Duration Trends",
                labels={"press_duration": "Press Duration (ms)", "time": "Timestamp"},
            )
            st.plotly_chart(press_duration_chart, use_container_width=True)
        else:
            st.warning("Required columns ('press_duration', 'time') are missing from the data.")

        # 3. Correlation Heatmap
        st.subheader("Correlation Heatmap")
        if set(["inter_key_interval", "press_duration"]).issubset(keyboard_data.columns):
            correlation_data = keyboard_data[["inter_key_interval", "press_duration"]].corr()

            fig, ax = plt.subplots()
            sns.heatmap(
                correlation_data,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                ax=ax,
                cbar=True,
            )
            st.pyplot(fig)
        else:
            st.warning("Not enough data to compute correlations.")
    else:
        st.warning("No abnormal keyboard data available.")
# Mouse Patterns
if section == "Mouse Patterns":
    st.subheader("Mouse Patterns")
    mouse_data = fetch_data(mouse_collection)
    if not mouse_data.empty:
        st.dataframe(mouse_data)
        st.subheader("Mouse Speed Over Time")
        mouse_speed_chart = px.line(mouse_data, x="time", y="speed", title="Mouse Speed Over Time")
        st.plotly_chart(mouse_speed_chart, use_container_width=True)
        st.subheader("Mouse Movement Flow")

        if mouse_data.empty:
            st.error("No data available for heatmap")
        else:
            # Convert records to a DataFrame
            st.dataframe(mouse_data)
            df = pd.DataFrame(mouse_data)
            print(df["x"], 'df')

            # Generate heatmap
            plt.figure(figsize=(10, 8))
            sns.kdeplot(x=df["x"], y=df["y"], cmap="Blues", color='Red', fill=True)
            plt.title("Mouse Flow Heatmap")
            plt.xlabel("X Coordinates")
            plt.ylabel("Y Coordinates")

            # Save the heatmap to a buffer and display it in Streamlit
            st.pyplot(plt)
    else:
        st.warning("No abnormal mouse data available.")
# Footer
st.markdown(
    """
    <footer class="bg-light text-center text-lg-start">
    <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
        © 2025 Abnormal Activity Monitoring System
    </div>
    </footer>
    """,
    unsafe_allow_html=True,
)
