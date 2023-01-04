import pprint
from datetime import datetime
from config import WEATHER_KEY
import requests
import re

message = input('Enter city name or coordinates: ')
TIME_FORMAT = '%H:%M:%S'
DATE_FORMAT = '%A, %d-%m-%Y'


def get_weather(WEATHER_KEY, message):
    response = ''
    if re.match('[A-Z]?[a-z]\.?', message):
        city = message
        url_with_name = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url_with_name).json()
    elif re.match('\d\.?,?\s?', message):
        latitude = message.split(', ')[0]
        longitude = message.split(', ')[1]
        url_with_coord = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url_with_coord).json()
    return response


def clear_data():
    response = get_weather(WEATHER_KEY, message=message)
    if response['cod'] == 200:
        # pprint.pprint(response)
        city_name = response['name']
        temperature = response['main']['temp']
        feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        weekday = datetime.fromtimestamp(response['dt']).strftime(DATE_FORMAT)
        sunset = datetime.fromtimestamp(response['sys']['sunset']).strftime(TIME_FORMAT)
        sunrise = datetime.fromtimestamp(response['sys']['sunrise']).strftime(TIME_FORMAT)
        description = response['weather'][0]['description']
        print(f'Today {weekday} in {city_name}: {description}')
        print(f'Temperature - {temperature}°C \nFeels like - {feels_like}°C')
        print(f'Humidity - {humidity}% \nSunrise at {sunrise} \nSunset at {sunset}')

    else:
        pprint.pprint(response)
        error_message = response['message']


clear_data()