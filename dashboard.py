import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from pandas._libs.tslibs.timestamps import Timestamp
import calender
sns.set(style='dark')

# Load Data
hour = pd.read_csv("hour.csv")

# Convert dteday to datetime
hour['dteday'] = pd.to_datetime(hour['dteday'])

# Function to display dashboard page
def display_dashboard():
    # Title for Bikeshare Dashboard (2011-2012)
    st.title("Bikeshare Dashboard (2011-2012)")

    # Sidebar for date filtering
    st.sidebar.subheader("Date Filtering")
    min_date = hour['dteday'].min()
    max_date = hour['dteday'].max()
    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

    # Convert start_date and end_date to Timestamp objects
    start_date = Timestamp(start_date)
    end_date = Timestamp(end_date)

    # Filter data by date range
    filtered_hour = hour[(hour['dteday'] >= start_date) & (hour['dteday'] <= end_date)]

    # Total rental information
    total_rentals = filtered_hour['cnt'].sum()

    # Additional business metrics
    average_daily_rentals = filtered_hour['cnt'].mean()

    # Calculate rental counts for each hour
    hourly_rentals = filtered_hour.groupby('hr')['cnt'].sum()

    # Find the hour with the highest rental count
    peak_hour = hourly_rentals.idxmax()
    peak_hour_count = hourly_rentals.max()

    # Business metrics layout
    business_metrics_layout = st.columns([1, 1, 1])
    with business_metrics_layout[0]:
        st.metric(label="Total Rentals", value=f"{total_rentals:,}")
    with business_metrics_layout[1]:
        st.metric(label="Average Daily Rentals", value=f"{average_daily_rentals:.2f}")
    with business_metrics_layout[2]:
        st.metric(label="Peak Rental Hour", value=f"{peak_hour}:00", delta=f"{peak_hour_count:,} rentals")

    # Title for Monthly Count of Bicycle Users
    st.subheader("Monthly Count of Bicycle Users (2011-2012)")

    # Create Dict for decide number month to name month
    month_labels = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Des"
    }
    
    # Set Figure
    plt.figure(figsize=(16,6))

    # Create lineplot for monthly count of bicycle users
    sns.lineplot(x=filtered_hour.resample('M', on='dteday').sum().index.month, y="cnt", data=filtered_hour.resample('M', on='dteday').sum(), color='blue')

    # Decide label X to name month
    plt.xticks(range(1, 13), [month_labels[month] for month in range(1, 13)])

    # Assign labels and title
    plt.xlabel("")
    plt.ylabel("Total Bicycle Users")
    plt.title("Monthly count of bicycle users")

    # Get the figure object
    fig = plt.gcf()

    # Show plot
    st.pyplot(fig)

    # Title for Count of Bicycle Users by Season
    st.subheader("Count of Bicycle users by Season")

    # Count the number of users by season
    season_users = filtered_hour.groupby("season")["cnt"].sum().reset_index()

    # Map season numbers to labels
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_users['season'] = season_users['season'].map(season_labels)

    # Determine the seasonal order
    season_order = season_users["season"].unique()

    # Create Barplot for count of Bicycle Users by season
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x="season", y="cnt", data=season_users, order=season_order, palette=["lightblue" if x != season_users['cnt'].max() else "darkblue" for x in season_users['cnt']])
    plt.xlabel("")
    plt.ylabel("Total Bicycle Users")
    plt.title("Count of Bicycle Users by Season")

    # Format y-axis labels
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])

    # Get the figure object
    fig = plt.gcf()

    # Show plot
    st.pyplot(fig)

    # Title for Count of Bicycle Users by Weekday
    st.subheader("Count of Bicycle users by Weekday")

    # Count the number of users by weekday
    weekday_users = filtered_hour.groupby("weekday")["cnt"].sum().reset_index()

    # Map weekday numbers to labels
    weekday_labels = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
    weekday_users['weekday'] = weekday_users['weekday'].map(weekday_labels)

    # Determine the weekday order
    weekday_order = weekday_users["weekday"].unique()

    # Create Barplot for count of Bicycle Use by weekday
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x="weekday", y="cnt", data=weekday_users, order=weekday_order, palette=["lightblue" if x != weekday_users['cnt'].max() else "darkblue" for x in weekday_users['cnt']])
    plt.xlabel("")
    plt.ylabel("Total Bicycle Users")
    plt.title("Count of Bicycle Users by Weekday")

    # Format y-axis labels
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])

    # Get the figure object
    fig = plt.gcf()

    # Show plot
    st.pyplot(fig)

    # Caption
    st.caption("Copyright by Deny Wisnu Saputro Sukisno")

    # Add GitHub and LinkedIn logos with links
    st.sidebar.write("[![GitHub](https://img.shields.io/badge/GitHub-DenyWisnuSS-blue?logo=github)](https://github.com/DenyWisnuSS)")
    st.sidebar.write("[![LinkedIn](https://img.shields.io/badge/LinkedIn-Deny%20Wisnu%20Saputro%20Sukisno-blue?logo=linkedin)](https://www.linkedin.com/in/denywsnu)")

# Function to display about page
def display_about():
    st.subheader("About This Dashboard")
    st.write("""
    This dashboard provides insights into bikeshare data from 2011 to 2012. 
    You can use the sidebar to filter the date range and explore various metrics and visualizations below.
             
    The Dashboard answer 3 question:
    - How is the trend in the number of bicycle users in recent years?
    - Which season has the most cyclists?
    - What are the usage patterns of bike-sharing services by day of the week?
             
    Provide several Business Metrics such as:
    1. Total Rentals
    2. Average Daily Rentals
    3. Peak Rental Hour 
    """)

# Check if the user has accessed the dashboard before
if "first_time_user" not in st.session_state:
    st.session_state["first_time_user"] = True

# Sidebar navigation
st.sidebar.subheader("Navigation")

# Add icons to the navigation menu
icon_dict = {
    "About": "ℹ️",
    "Dashboard": "📊"
}

# Create buttons with icons and display corresponding pages
for option in icon_dict:
    if st.sidebar.button(f"{icon_dict[option]} {option}"):
        if option == "About":
            display_about()
        elif option == "Dashboard":
            display_dashboard()

# If it's the user's first time accessing the app, display the dashboard automatically
if st.session_state["first_time_user"]:
    display_dashboard()
    st.session_state["first_time_user"] = False
