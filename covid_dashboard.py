# Importing Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Doing Basic Headings
st.title("🌍 COVID-19 Trend Dashboard")
st.subheader("📈 Analyze COVID-19 daily trends, cases, deaths, and vaccinations across countries.")
st.set_page_config(layout="wide")

# Selecting Country
select_country = st.selectbox("🌐 Select Country", ["India", "United Kingdom", "United States", "Brazil", "Russia"])

# Loading Data 
df = pd.read_csv("covid_data.csv")

# Sorting Data and Null Values
country_df = df[df['location'] == select_country]
dropping_country = country_df.dropna(subset = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'people_vaccinated', 'people_fully_vaccinated'])
dropping_country['date'] = pd.to_datetime(dropping_country['date'])

# Total Cases in Selected Country
total_cases_country = dropping_country.sort_values('date').iloc[-1]['total_cases']

# Total Deaths in Selected Country
total_deaths_country = dropping_country.sort_values('date').iloc[-1]['total_deaths']

# Total People Vaccinated in Selected Country
total_vaccine_country = dropping_country.sort_values('date').iloc[-1]['people_fully_vaccinated']

# Making Total Area for Cases, Deaths and Vaccinated
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label = "🦠 Total Cases", value = f"{total_cases_country:,.0f}")
with col2:
    st.metric(label = "💀 Total Deaths", value = f"{total_deaths_country:,.0f}")
with col3:
    st.metric(label = "💉 Total Fully Vaccinated", value = f"{total_vaccine_country:,.0f}")


# Create a line chart of new_cases over time
st.subheader(f"📊 Daily New COVID-19 Cases in {select_country}")
fig, ax = plt.subplots(figsize = (10, 6))
ax.plot(dropping_country['date'], dropping_country['new_cases'])
ax.set_xlabel("Years")
ax.set_ylabel("New Cases(in millions)")
ax.grid(True)
ax.set_title(f"📊 Daily New COVID-19 Cases in {select_country}")
plt.tight_layout()
st.pyplot(fig)

# Create a line chart of new_deaths over time
st.subheader(f"☠️ Daily New COVID-19 Deaths in {select_country}")
fig, ax = plt.subplots(figsize = (10, 6))
ax.plot(dropping_country['date'], dropping_country['new_deaths'], color = 'red')
ax.set_xlabel("Years")
ax.set_ylabel("New Deaths")
ax.grid(True)
ax.set_title(f"☠️ Daily COVID-19 Deaths in {select_country}")
plt.tight_layout()
st.pyplot(fig)

# Data for Bar chart(Cases)
st.subheader(f"📊 Daily New COVID-19 Cases by Country")
countries = ['Brazil', 'Russia', 'India', 'United States', 'United Kingdom']
country_cases = []
for country in countries:
    country_data = df[df['location'] == country]
    clean_data = country_data.dropna(subset = {'total_cases', 'total_deaths'})
    clean_data['date'] = pd.to_datetime(clean_data['date'])
    clean_data = clean_data.sort_values('date')

    if not clean_data.empty:
        latest_case = clean_data.sort_values('date').iloc[-1]['total_cases']
        country_cases.append(latest_case)
    else:
        country_cases.append(0)

# Bar chart: Total Cases by Country
fig, ax = plt.subplots(figsize = (10, 6))
ax.bar(countries, country_cases, color = 'orange')
ax.set_xlabel('Countries')
ax.set_ylabel('Total Cases (In Millions)')
ax.set_title("📊 Total COVID-19 Cases by Country")
st.pyplot(fig)

# Data for Bar Chart(Deaths)
st.subheader(f"📊 Daily New COVID-19 Deaths by Country")
country_deaths = []
for country_deaths_loop in countries:
    country_data_deaths = df[df['location'] == country_deaths_loop]
    clean_data_deaths = country_data_deaths.dropna(subset = {'total_cases', 'total_deaths'})
    clean_data_deaths['date'] = pd.to_datetime(clean_data_deaths['date'])
    clean_data_deaths = clean_data_deaths.sort_values('date')

    if not clean_data.empty:
        latest_deaths = clean_data_deaths.sort_values('date').iloc[-1]['total_deaths']
        country_deaths.append(latest_deaths)
    else:
        country_deaths.append(0)

# Bar chart: Total Deaths by Country
fig, ax = plt.subplots(figsize = (10, 6))
ax.bar(countries, country_deaths, color = 'red')
ax.set_xlabel('Countries')
ax.set_ylabel('Total Deaths (In Millions)')
ax.set_title("📊 Total COVID-19 Deaths by Country")
st.pyplot(fig)

# Adding Sidebar for New Cases and Deaths
st.sidebar.header("Choose Metric")
sidebar = st.sidebar.radio("", ["Total New Cases", "Total New Deaths"])
if sidebar == "Total New Cases":
    total_case = dropping_country['new_cases'].sum()
    avg_case = dropping_country['new_cases'].mean()
    maxi_case = dropping_country['new_cases'].max()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.sidebar.metric(label = "🦠 Total Cases", value = f"{total_case:,.0f}")
    with col2:
        st.sidebar.metric(label = "🦠 Average Cases", value = f"{avg_case:,.0f}")
    with col3:
        st.sidebar.metric(label = "🦠 Maximum Cases in One Day", value = f"{maxi_case:,.0f}")
    
elif sidebar == "Total New Deaths":
    total_death = dropping_country['new_deaths'].sum()
    avg_death = dropping_country['new_deaths'].mean()
    maxi_death = dropping_country['new_deaths'].max()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.sidebar.metric(label = "☠️ Total Deaths", value = f"{total_death:,.0f}")
    with col2:
        st.sidebar.metric(label = "☠️ Average Deaths", value = f"{avg_death:,.0f}")
    with col3:
        st.sidebar.metric(label = "☠️ Maximum Deaths in One Day", value = f"{maxi_death:,.0f}")
