import openmeteo_requests
import requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://api.open-meteo.com/v1/forecast"


def convert_city_to_lat_lon(city):
    language = 'ru' if 'а' < city[0].lower() < 'я' else "en"
    url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language={language}"
    try:
        request = requests.get(url_geo).json()
        full_name = (request['results'][0]['country'] + ", " + request['results'][0]['admin1']
                     + ", " + request['results'][0]['name'])
        return request['results'][0]['latitude'], request['results'][0]['longitude'], full_name
    except:
        return None, None, None


def give_condition_df(city, days):
    lat, lon, full_name = convert_city_to_lat_lon(city)
    if full_name is None:
        return None, None
    condition_df = give_condition_df_from_open_meteo(lat, lon, days)
    return condition_df, full_name


def give_condition_df_from_open_meteo(lat, lon, days):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "forecast_days": days
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
            "temperature": hourly_temperature_2m,
            "humidity": hourly_relative_humidity_2m,
            "precipitation": hourly_precipitation,
            "wind_speed": hourly_wind_speed_10m
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        return hourly_dataframe
    except:
        return None


def get_weather_description(weather_code):
    weather_mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle, light",
        53: "Drizzle, moderate",
        55: "Drizzle, heavy",
        61: "Rain, light",
        63: "Rain, moderate",
        65: "Rain, heavy",
        71: "Snow fall, light",
        73: "Snow fall, moderate",
        75: "Snow fall, heavy",
        77: "Snow grains",
        80: "Showers, light",
        81: "Showers, moderate",
        82: "Showers, heavy",
        95: "Thunderstorm, light",
        96: "Thunderstorm with hail, light",
        99: "Thunderstorm with hail, heavy"
    }
    return weather_mapping.get(weather_code, "Unknown weather code")


def get_simple_weather_from_lat_lon(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "weather_code"]
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_weather_code = current.Variables(1).Value()

    return get_weather_description(current_weather_code) + ", " + str(round(current_temperature_2m)) + "°C"


def convert_cities_to_df(cities):
    lat_list = []
    lon_list = []
    weather_list = []
    for city in cities:
        lat, lon, full_name = convert_city_to_lat_lon(city)
        weather_list.append(get_simple_weather_from_lat_lon(lat, lon))
        lat_list.append(lat)
        lon_list.append(lon)
    df_cities = pd.DataFrame({
        'Город': cities,
        'Погода': weather_list,
        'lat': lat_list,
        'lon': lon_list
    })
    return df_cities


if __name__ == '__main__':
    print(give_condition_df('Moscow', 3))
