import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Siem Reap Weather Dashboard", layout="centered")

API_KEY = "c6c0419ab74f40d8a6085259250806"  # Your API key
LOCATION = "Siem Reap"

def get_weather(api_key, location):
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": 3,
        "aqi": "no",
        "alerts": "no"
    }
    response = requests.get(url, params=params)
    return response.json()

data = get_weather(API_KEY, LOCATION)

if "error" in data:
    st.error(f"API Error: {data['error']['message']}")
else:
    st.title(f"🌤️ Weather Dashboard - {LOCATION}")

    # Current weather
    current = data['current']
    condition = current['condition']['text']
    temp_c = current['temp_c']
    humidity = current['humidity']
    wind_kph = current['wind_kph']
    last_updated = current['last_updated']

    st.header("Current Weather")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Temperature: {temp_c} °C")
        st.write(f"Condition: {condition}")
    with col2:
        st.write(f"Humidity: {humidity} %")
        st.write(f"Wind Speed: {wind_kph} kph")
    st.write(f"Last updated: {last_updated}")

    # Forecast
    st.header("3-Day Forecast")
    forecast_days = data['forecast']['forecastday']
    for day in forecast_days:
        date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A, %b %d')
        day_condition = day['day']['condition']['text']
        max_temp = day['day']['maxtemp_c']
        min_temp = day['day']['mintemp_c']
        chance_of_rain = day['day'].get('daily_chance_of_rain', 'N/A')

        st.subheader(date)
        st.write(f"Condition: {day_condition}")
        st.write(f"Max Temp: {max_temp} °C")
        st.write(f"Min Temp: {min_temp} °C")
        st.write(f"Chance of Rain: {chance_of_rain} %")
        st.markdown("---")