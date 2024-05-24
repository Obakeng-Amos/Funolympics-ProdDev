import streamlit as st
import pandas as pd
import requests
import time
import datetime
import re
import altair as alt  # Import Altair
import numpy as np
import plotly.express as px
import warnings 
from collections import defaultdict
warnings.filterwarnings('ignore')

# Set page width to wide
st.set_page_config(page_title="FunOlympics Dashboard", layout="wide")

# Function to fetch logs from Flask API
def fetch_logs(num_logs=10000):
    response = requests.get(f"http://localhost:5000/logs?num_logs={num_logs}")
    if response.status_code == 200:
        logs = response.json()
        df = pd.DataFrame(logs)
        return df
    else:
        st.error("Failed to fetch logs from server.")
        return pd.DataFrame()

def sample_logs(logs_df):
    """
    Randomly samples a number of records from the given logs DataFrame.

    Parameters:
    logs_df (pd.DataFrame): The DataFrame containing log records.

    Returns:
    pd.DataFrame: A DataFrame containing the sampled log records.
    """
    num_records_to_sample = np.random.randint(9000, 10001)
    num_records_to_sample = min(num_records_to_sample, len(logs_df))
    sampled_df = logs_df.sample(n=num_records_to_sample, random_state=42)
    return sampled_df

df = sample_logs(fetch_logs())

# Title of dashboard
st.title("FunOlympics Dashboard 🏅")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# FunOlympics logo & Sidebar description
with st.sidebar:
    st.markdown("<div style='display: flex; align-items: center; width: 100px;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/1200px-Olympic_rings_without_rims.svg.png' width=100 /><h1 style='display:inline-block; margin-left: 10px;'>FunOlympics</h1></div>", unsafe_allow_html=True)
    st.markdown("This dashboard allows you to analyze :chart_with_upwards_trend: FunOlympics data from a streaming platform.")

    csv_button = st.button("Download CSV")
    if csv_button:
        with st.spinner('Fetching data...'):
            progress_bar = st.progress(0)
            for i in range(0, 101, 20):
                time.sleep(0.1)
                progress_bar.progress(i)
            df = fetch_logs()
            progress_bar.progress(100)

        csv = df.to_csv(index = False)
        st.download_button(
            label = "Download CSV",
            data = csv,
            file_name = "Funolympics_data.csv",
            mime = "text/csv"
        )

# Sidebar filters for main interests
view_by = st.sidebar.selectbox('View Main Interests By:', ['Sports', 'Country'])
country_filter = st.sidebar.selectbox('Select Country:', df['Country'].unique())
view_by_time = st.sidebar.selectbox('Select Time Granularity:', ['Day', 'Month'])
selected_sports = st.sidebar.multiselect('Select Sports:', df['Sport'].unique(), default=df['Sport'].unique()[:5])

# Real-time update placeholders
data_placeholder = st.empty()
metrics_placeholder = st.empty()
interests_placeholder = st.empty()
geo_placeholder = st.empty()
part1, part2, part3 = st.columns(3)
device_placeholder = part1.empty()
status_placeholder = part2.empty()
browser_placeholder = part3.empty()
trend_placeholder = st.empty()
sports_placeholder = st.empty()
heatmap_placeholder = st.empty()
df_placeholder = st.empty()  # Placeholder for DataFrame display

# Real-time update loop
while True:
    # Fetch data
    df = sample_logs(fetch_logs())

    # Metrics calculations
    total_visits = len(df)
    average_response_time = df['Time_Elapsed'].mean()
    total_countries = df['Country'].nunique()

    # Display metrics in columns
    with metrics_placeholder.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin: 10px; box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;">
                    <h3 style="color: #6a0dad;"> Number of Visits</h3>
                    <h1 style="color: #6a0dad;">{total_visits}</h1>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin: 10px; box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;">
                    <h3 style="color: #6a0dad;"> Avg Response Time</h3>
                    <h1 style="color: #6a0dad;">{average_response_time:.2f} ms</h1>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin: 10px; box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;">
                    <h3 style="color: #6a0dad;"> Countries</h3>
                    <h1 style="color: #6a0dad;">{total_countries}</h1>
                </div>
            """, unsafe_allow_html=True)


    with interests_placeholder.container():
        if view_by == 'Sports':
            st.subheader('Main Interests Based on Selected/Viewed Sports')
            sports_interest = df['Sport'].value_counts().reset_index()
            sports_interest.columns = ['Sport', 'Count']
            col1, col2 = st.columns([3, 1])
            with col1:
                fig = px.bar(sports_interest, x='Sport', y='Count', title='Main Interests Based on Selected/Viewed Sports', labels={'Sport': 'Sport', 'Count': 'Number of Views'})
                st.plotly_chart(fig)
            with col2:
                st.write(sports_interest)
        else:
            st.subheader('Main viewed Sports Based on Country')
            country_data = df[df['Country'] == country_filter]
            country_sports_interest = country_data['Sport'].value_counts().reset_index()
            country_sports_interest.columns = ['Sport', 'Count']
            col1, col2 = st.columns([3, 1])
            with col1:
                fig = px.bar(country_sports_interest, x='Sport', y='Count', title=f'Views per Sport in {country_filter}', labels={'Sport': 'Sport', 'Count': 'Number of Views'})
                st.plotly_chart(fig)
            with col2:
                st.write(country_sports_interest)

    # Geographic Distribution of Views
    with geo_placeholder.container():
        #st.subheader('Geographic Distribution of Views')
        country_views = df['Country'].value_counts().reset_index()
        country_views.columns = ['Country', 'Views']
        fig_geo = px.choropleth(
            country_views,
            locations="Country",
            locationmode='country names',
            color="Views",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Geographic Distribution of Views"
        )
        fig_geo.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            title=dict(
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    # Regular expressions to match different devices
    windows_pattern = re.compile(r'Windows|Win')
    mac_pattern = re.compile(r'Macintosh|Mac OS')
    iphone_pattern = re.compile(r'iPhone')
    ipad_pattern = re.compile(r'iPad')
    android_pattern = re.compile(r'Android')

    # Regular expressions to match different browsers
    firefox_pattern = re.compile(r'Firefox')
    chrome_pattern = re.compile(r'Chrome')
    safari_pattern = re.compile(r'Safari')
    edge_pattern = re.compile(r'Edg')

    # Function to extract device type from user agent
    def extract_device(user_agent):
        if re.search(windows_pattern, user_agent):
            return 'Windows'
        elif re.search(mac_pattern, user_agent):
            return 'Mac'
        elif re.search(iphone_pattern, user_agent):
            return 'iPhone'
        elif re.search(ipad_pattern, user_agent):
            return 'iPad'
        elif re.search(android_pattern, user_agent):
            return 'Android'
        else:
            return 'Other'

    # Function to extract browser type from user agent
    def extract_browser(user_agent):
        if re.search(firefox_pattern, user_agent):
            return 'Firefox'
        elif re.search(chrome_pattern, user_agent):
            return 'Chrome'
        elif re.search(safari_pattern, user_agent):
            return 'Safari'
        elif re.search(edge_pattern, user_agent):
            return 'Edge'
        else:
            return 'Other'

    # Device and Browser Distribution
    df['Device'] = df['User_Agent'].apply(lambda x: extract_device(x))
    df['Browser'] = df['User_Agent'].apply(lambda x: extract_browser(x))
    device_distribution = df['Device'].value_counts()
    browser_distribution = df['Browser'].value_counts()
    status_code_distribution = df['Status_Code'].value_counts()

    with device_placeholder.container():
        fig_device = px.pie(device_distribution, values=device_distribution.values, names=device_distribution.index, hole=0.5, 
                            title='Distribution of Traffic by Device Type', color_discrete_sequence=px.colors.qualitative.Set3)
        fig_device.update_traces(textinfo='percent+label', pull=[0.1]*len(device_distribution), textposition='inside')
        fig_device.update_layout(showlegend=False)
        st.plotly_chart(fig_device, use_container_width=True)

    with status_placeholder.container():
        fig_status = px.pie(status_code_distribution, values=status_code_distribution.values, names=status_code_distribution.index, hole=0.5, 
                            title='Distribution of Traffic by Status Code', color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig_status.update_traces(textinfo='percent')
        fig_status.update_layout(legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.1))
        st.plotly_chart(fig_status, use_container_width=True)

    with browser_placeholder.container():
        fig_browser = px.pie(browser_distribution, values=browser_distribution.values, names=browser_distribution.index, 
                             title='Distribution of Browsers', hole=0.5, color_discrete_sequence=px.colors.qualitative.Set2)
        fig_browser.update_traces(textinfo='percent', pull=[0.1]*len(browser_distribution), textposition='inside')
        fig_browser.update_layout(showlegend=True)
        st.plotly_chart(fig_browser, use_container_width=True)

    # Trend of Views Over Time
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y:%H:%M:%S')
    df['Month'] = df['Timestamp'].dt.month_name()
    df['Day'] = df['Timestamp'].dt.day
    df['Year'] = df['Timestamp'].dt.year

    with trend_placeholder.container():
        st.subheader('Trend of Views Over Time')
        if view_by_time == 'Day':
            time_data = df.groupby(['Day', 'Month', 'Year']).size().reset_index(name='Views')
            time_data['Date'] = pd.to_datetime(time_data['Day'].astype(str) + '-' + time_data['Month'] + '-' + time_data['Year'].astype(str), format='%d-%B-%Y')
            time_data = time_data.sort_values('Date')
            fig = px.line(time_data, x='Date', y='Views', title='Trend of Views Over Time', labels={'Date': 'Date', 'Views': 'Number of Views'})
        else:
            time_data = df.groupby(['Month', 'Year']).size().reset_index(name='Views')
            time_data['Month'] = pd.Categorical(time_data['Month'], categories=[
                'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
            time_data = time_data.sort_values(['Year', 'Month'])
            fig = px.line(time_data, x='Month', y='Views', title='Trend of Views Over Time', labels={'Month': 'Month', 'Views': 'Number of Views'})
        st.plotly_chart(fig, use_container_width=True)

    # Sports Popularity Over Time
    with sports_placeholder.container():
        sports_data = df[df['Sport'].isin(selected_sports)]
        sports_data['Date'] = sports_data['Timestamp'].dt.to_period('M').astype(str)
        sports_trends = sports_data.groupby(['Date', 'Sport']).size().reset_index(name='Views')
        fig = px.line(sports_trends, x='Date', y='Views', color='Sport', title='Sports Popularity Over Time', labels={'Date': 'Date', 'Views': 'Number of Views'})
        st.plotly_chart(fig, use_container_width=True)

    # Peak Viewership Hours
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()

    with heatmap_placeholder.container():
        #st.subheader('Peak Viewership Hours')
        heatmap_data = df.groupby(['Hour', 'DayOfWeek']).size().reset_index(name='Views')
        heatmap_data['DayOfWeek'] = pd.Categorical(heatmap_data['DayOfWeek'], categories=[
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
        heatmap_data = heatmap_data.pivot(index='Hour', columns='DayOfWeek', values='Views')
        fig = px.imshow(heatmap_data, aspect="auto", title='Peak Viewership Hours', labels={'x': 'Day of Week', 'y': 'Hour of Day', 'color': 'Number of Views'})
        fig.update_layout(xaxis_title='Day of Week', yaxis_title='Hour of Day')
        st.plotly_chart(fig, use_container_width=True)
    
    # Display the DataFrame
    with df_placeholder.container():
        st.subheader('Data')
        st.write(df)

    # Sleep for a certain period before refreshing
    time.sleep(3)  # Refresh every 3 seconds