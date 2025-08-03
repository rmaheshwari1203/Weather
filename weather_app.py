import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time

# Set page config for a beautiful UI
st.set_page_config(
    page_title="🌤️ Weather Forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .forecast-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .location-input {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API configuration - Using free APIs (no API key required!)
GEOLOCATION_API_URL = "http://ip-api.com/json/"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def get_user_location_by_ip():
    """Get user location using IP geolocation"""
    try:
        response = requests.get(GEOLOCATION_API_URL)
        if response.status_code == 200:
            data = response.json()
            return {
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'city': data.get('city'),
                'country': data.get('country')
            }
    except:
        return None
    return None

def get_weather_data(lat, lon):
    """Fetch current weather and forecast data using Open-Meteo (free!)"""
    try:
        # Open-Meteo API call
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 
                       'precipitation', 'weather_code', 'wind_speed_10m', 'pressure_msl'],
            'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min', 
                     'precipitation_sum', 'wind_speed_10m_max'],
            'timezone': 'auto',
            'forecast_days': 7
        }
        
        response = requests.get(WEATHER_API_URL, params=params)
        
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
    return None

def get_weather_by_city(city):
    """Get weather data by city name using free geocoding"""
    try:
        # Get coordinates from city name using Open-Meteo geocoding
        geo_params = {'name': city, 'count': 1, 'language': 'en', 'format': 'json'}
        geo_response = requests.get(GEOCODING_API_URL, params=geo_params)
        
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            if geo_data.get('results'):
                result = geo_data['results'][0]
                lat = result['latitude']
                lon = result['longitude']
                return get_weather_data(lat, lon), result
    except Exception as e:
        st.error(f"Error finding city: {e}")
    return None, None

def get_weather_emoji(weather_code):
    """Get emoji based on WMO weather code (Open-Meteo format)"""
    weather_emojis = {
        0: '☀️',    # Clear sky
        1: '🌤️',   # Mainly clear
        2: '⛅',    # Partly cloudy
        3: '☁️',    # Overcast
        45: '🌫️',  # Fog
        48: '🌫️',  # Depositing rime fog
        51: '🌦️',  # Light drizzle
        53: '🌦️',  # Moderate drizzle
        55: '🌧️',  # Dense drizzle
        56: '🌧️',  # Light freezing drizzle
        57: '🌧️',  # Dense freezing drizzle
        61: '🌧️',  # Slight rain
        63: '🌧️',  # Moderate rain
        65: '🌧️',  # Heavy rain
        66: '🌧️',  # Light freezing rain
        67: '🌧️',  # Heavy freezing rain
        71: '❄️',  # Slight snow fall
        73: '❄️',  # Moderate snow fall
        75: '❄️',  # Heavy snow fall
        77: '❄️',  # Snow grains
        80: '🌦️',  # Slight rain showers
        81: '🌧️',  # Moderate rain showers
        82: '🌧️',  # Violent rain showers
        85: '❄️',  # Slight snow showers
        86: '❄️',  # Heavy snow showers
        95: '⛈️',  # Thunderstorm
        96: '⛈️',  # Thunderstorm with slight hail
        99: '⛈️'   # Thunderstorm with heavy hail
    }
    return weather_emojis.get(weather_code, '🌤️')

def get_weather_description(weather_code):
    """Get weather description from WMO code"""
    descriptions = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        56: 'Light freezing drizzle',
        57: 'Dense freezing drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        66: 'Light freezing rain',
        67: 'Heavy freezing rain',
        71: 'Slight snow fall',
        73: 'Moderate snow fall',
        75: 'Heavy snow fall',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail'
    }
    return descriptions.get(weather_code, 'Unknown')

def display_current_weather(weather_data, location_info=None):
    """Display current weather information"""
    current = weather_data['current']
    
    # Get location name
    if location_info:
        location_name = f"{location_info.get('name', 'Unknown')}, {location_info.get('country', '')}"
    else:
        location_name = "Current Location"
    
    st.markdown(f"""
    <div class="weather-card">
        <h1>{get_weather_emoji(current['weather_code'])} {location_name}</h1>
        <h2>{current['temperature_2m']:.1f}°C</h2>
        <h3>{get_weather_description(current['weather_code'])}</h3>
        <p>Feels like {current['apparent_temperature']:.1f}°C</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Weather metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💧 Humidity</h4>
            <h3>{current['relative_humidity_2m']:.0f}%</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🌪️ Wind Speed</h4>
            <h3>{current['wind_speed_10m']:.1f} km/h</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📊 Pressure</h4>
            <h3>{current['pressure_msl']:.0f} hPa</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        precipitation = current.get('precipitation', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4>🌧️ Precipitation</h4>
            <h3>{precipitation:.1f} mm</h3>
        </div>
        """, unsafe_allow_html=True)

def display_forecast(weather_data):
    """Display 5-day weather forecast"""
    daily = weather_data['daily']
    
    st.markdown("## 📅 7-Day Forecast")
    
    # Display forecast cards (skip today, show next 6 days)
    cols = st.columns(6)
    
    for i in range(1, 7):  # Skip today (index 0), show next 6 days
        with cols[i-1]:
            date = datetime.fromisoformat(daily['time'][i])
            day_name = date.strftime("%A")
            date_str = date.strftime("%m/%d")
            
            weather_code = daily['weather_code'][i]
            max_temp = daily['temperature_2m_max'][i]
            min_temp = daily['temperature_2m_min'][i]
            precipitation = daily['precipitation_sum'][i] if daily['precipitation_sum'][i] else 0
            
            st.markdown(f"""
            <div class="forecast-card">
                <h4>{day_name}</h4>
                <p>{date_str}</p>
                <h2>{get_weather_emoji(weather_code)}</h2>
                <h3>{max_temp:.1f}°C</h3>
                <p>{min_temp:.1f}°C</p>
                <p>{get_weather_description(weather_code)}</p>
                <small>🌧️ {precipitation:.1f}mm</small>
            </div>
            """, unsafe_allow_html=True)

def main():
    # App header
    st.markdown("""
    <div class="main-header">
        <h1>🌤️ Weather Forecast App</h1>
        <p>Get real-time weather updates and forecasts - Completely Free!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'location_detected' not in st.session_state:
        st.session_state.location_detected = False
    if 'weather_data' not in st.session_state:
        st.session_state.weather_data = None
    if 'location_info' not in st.session_state:
        st.session_state.location_info = None
    
    # Location detection section
    if not st.session_state.location_detected:
        st.markdown("""
        <div class="location-input">
            <h2>📍 Location Required</h2>
            <p>We need your location to provide accurate weather information</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌍 Auto-Detect Location", use_container_width=True):
                with st.spinner("🔍 Detecting your location..."):
                    location = get_user_location_by_ip()
                    if location and location['lat'] and location['lon']:
                        weather_data = get_weather_data(location['lat'], location['lon'])
                        if weather_data:
                            st.session_state.weather_data = weather_data
                            st.session_state.location_detected = True
                            st.session_state.auto_location = location
                            st.session_state.location_info = {
                                'name': location['city'],
                                'country': location['country']
                            }
                            st.success(f"📍 Location detected: {location['city']}, {location['country']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to fetch weather data")
                    else:
                        st.error("Could not auto-detect location. Please enter manually.")
        
        with col2:
            with st.form("manual_location"):
                city_input = st.text_input("🏙️ Enter City Name", placeholder="e.g., London, New York, Tokyo")
                submit_button = st.form_submit_button("Get Weather", use_container_width=True)
                
                if submit_button and city_input:
                    with st.spinner(f"🌡️ Getting weather for {city_input}..."):
                        weather_data, location_info = get_weather_by_city(city_input)
                        if weather_data and location_info:
                            st.session_state.weather_data = weather_data
                            st.session_state.location_detected = True
                            st.session_state.manual_city = city_input
                            st.session_state.location_info = location_info
                            st.success(f"✅ Weather data loaded for {location_info['name']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ Could not find weather data for '{city_input}'. Please check the city name.")
    
    # Display weather data
    if st.session_state.location_detected and st.session_state.weather_data:
        # Refresh and change location buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Refresh Weather", use_container_width=True):
                # Refresh weather data
                if 'auto_location' in st.session_state:
                    location = st.session_state.auto_location
                    weather_data = get_weather_data(location['lat'], location['lon'])
                elif 'manual_city' in st.session_state:
                    weather_data, location_info = get_weather_by_city(st.session_state.manual_city)
                    if location_info:
                        st.session_state.location_info = location_info
                
                if weather_data:
                    st.session_state.weather_data = weather_data
                    st.success("🔄 Weather data refreshed!")
                    time.sleep(1)
                    st.rerun()
        
        with col3:
            if st.button("📍 Change Location", use_container_width=True):
                # Reset all location-related session state
                for key in ['location_detected', 'weather_data', 'auto_location', 'manual_city', 'location_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        # Display current weather
        display_current_weather(st.session_state.weather_data, st.session_state.location_info)
        
        # Display forecast
        display_forecast(st.session_state.weather_data)
        
        # Additional information
        st.markdown("---")
        current = st.session_state.weather_data['current']
        
        col1, col2 = st.columns(2)
        with col1:
            current_time = datetime.now().strftime("%H:%M")
            st.markdown(f"""
            ### 🕐 Current Time
            - **Local Time:** {current_time}
            - **Last Updated:** {datetime.now().strftime("%H:%M:%S")}
            """)
        
        with col2:
            st.markdown(f"""
            ### 🌡️ Temperature Details
            - **Current:** {current['temperature_2m']:.1f}°C
            - **Feels like:** {current['apparent_temperature']:.1f}°C
            - **Humidity:** {current['relative_humidity_2m']:.0f}%
            """)
        
        # Data source attribution
        st.markdown("---")
        st.markdown("*Weather data provided by [Open-Meteo](https://open-meteo.com/) - Free weather API*")

if __name__ == "__main__":
    main()