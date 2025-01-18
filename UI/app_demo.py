import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Dummy Data with random values
np.random.seed(42)
file_access_data = pd.DataFrame({
    "time": pd.date_range(start="2024-01-01", periods=100, freq="h"),
    "event_type": np.random.choice(["read", "write", "delete"], 100),
})

keyboard_data = pd.DataFrame({
    "time": pd.date_range(start="2024-01-01", periods=100, freq="h"),
    "inter_key_interval": np.random.uniform(0.1, 1.0, 100),
})

mouse_data = pd.DataFrame({
    "time": pd.date_range(start="2024-01-01", periods=100, freq="h"),
    "speed": np.random.uniform(5, 30, 100),
})

# Utility function to fetch dummy data
def fetch_data_dummy(data, limit=1000):
    return data.head(limit)

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Choose a section:",
    ["Dashboard", "File Access Patterns", "Keyboard Patterns", "Mouse Patterns"]
)

# Custom CSS for UI styling
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #4CAF50;
            text-align: center;
        }
        .section-header {
            font-size: 1.8rem;
            margin-bottom: 15px;
            color: #2A9D8F;
        }
        .dataframe-container {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            background-color: #f9f9f9;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-title'>Abnormal Activity Monitoring Dashboard</div>", unsafe_allow_html=True)

if section == "Dashboard":
    st.markdown("<div class='section-header'>Overview</div>", unsafe_allow_html=True)
    st.markdown("This dashboard visualizes abnormal patterns detected in File Access, Keyboard, and Mouse data.")

    # Overview metrics
    file_count = len(file_access_data)
    keyboard_count = len(keyboard_data)
    mouse_count = len(mouse_data)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.metric("Abnormal File Events", file_count)
    with col2:
        st.metric("Abnormal Keyboard Events", keyboard_count)
    with col3:
        st.metric("Abnormal Mouse Events", mouse_count)

    # Frequency over time
    st.markdown("<div class='section-header'>Abnormal Events Over Time</div>", unsafe_allow_html=True)
    file_time_chart = px.line(
        file_access_data, x="time", y=file_access_data.index,
        title="File Events Over Time", line_shape="spline",
        labels={"index": "Event Count", "time": "Timestamp"}
    )
    st.plotly_chart(file_time_chart, use_container_width=True)

elif section == "File Access Patterns":
    st.markdown("<div class='section-header'>File Access Patterns</div>", unsafe_allow_html=True)
    file_data = fetch_data_dummy(file_access_data)
    if not file_data.empty:

        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(file_data, height=300, width=700)
        st.markdown("</div>", unsafe_allow_html=True)

        # Visualizations
        st.markdown("<div class='section-header'>Event Types Distribution</div>", unsafe_allow_html=True)
        event_type_chart = px.pie(
            file_data, names="event_type", title="Event Types Distribution",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(event_type_chart, use_container_width=True)

        st.markdown("<div class='section-header'>File Access Timeline</div>", unsafe_allow_html=True)
        file_time_chart = px.area(
            file_data, x="time", y=file_data.index, title="File Events Timeline",
            labels={"index": "Event Count", "time": "Timestamp"},
            color_discrete_sequence=["#00C49F"]
        )
        st.plotly_chart(file_time_chart, use_container_width=True)
    else:
        st.warning("No abnormal file access data available.")

elif section == "Keyboard Patterns":
    st.markdown("<div class='section-header'>Keyboard Patterns</div>", unsafe_allow_html=True)
    keyboard_data_sample = fetch_data_dummy(keyboard_data)
    if not keyboard_data_sample.empty:
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(keyboard_data_sample, height=300, width=700)
        st.markdown("</div>", unsafe_allow_html=True)

        # Visualizations
        st.markdown("<div class='section-header'>Inter-Key Interval Distribution</div>", unsafe_allow_html=True)
        interval_chart = px.histogram(
            keyboard_data_sample, x="inter_key_interval", title="Inter-Key Interval Distribution",
            color_discrete_sequence=["#FF6F61"]
        )
        st.plotly_chart(interval_chart, use_container_width=True)
    else:
        st.warning("No abnormal keyboard data available.")

elif section == "Mouse Patterns":
    st.markdown("<div class='section-header'>Mouse Patterns</div>", unsafe_allow_html=True)
    mouse_data_sample = fetch_data_dummy(mouse_data)
    if not mouse_data_sample.empty:
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(mouse_data_sample, height=300, width=700)
        st.markdown("</div>", unsafe_allow_html=True)

        # Visualizations
        st.markdown("<div class='section-header'>Mouse Speed Over Time</div>", unsafe_allow_html=True)
        mouse_speed_chart = px.scatter(
            mouse_data_sample, x="time", y="speed", title="Mouse Speed Over Time",
            size="speed", color="speed",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(mouse_speed_chart, use_container_width=True)
    else:
        st.warning("No abnormal mouse data available.")
