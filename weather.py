import pprint
from datetime import datetime
from config import WEATHER_KEY
import requests
import re
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

TIME_FORMAT = '%H:%M:%S'
DATE_FORMAT = '%A, %d-%m-%Y'
EXPECT_CITY = range(1)
WEATHER_DICT = {
    'Clear': '☀',
    'Clouds': '☁',
    'Rain': '🌧',
    'Drizzle': '🌧',
    'Thunderstorm': '⛈',
    'mist': '🌫',
    'Snow': '❄',
}
WIND_DICT = {
    0: 'N',
    22.5: 'NNE',
    45: 'NE',
    67.5: 'ENE',
    90: 'E',
    112.5: 'ESE',
    135: 'SE',
    157.5: 'SSE',
    180: 'S',
    202.5: 'SSW',
    225: 'SW',
    247.5: 'WSW',
    270: 'W',
    292.5: 'WNW',
    315: 'NW',
    337.5: 'NNW',
    360: 'N'
}


def get_city(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me city name or coordinates")
    return EXPECT_CITY


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


def get_emoji(main_weather):
    for key in WEATHER_DICT.keys():
        if main_weather == key:
            emoji = WEATHER_DICT[key]
            return emoji


def get_wind_direction(wind_deg):
    for key in WIND_DICT.keys():
        if wind_deg == key:
            wind_direction = WIND_DICT[key]
            return wind_direction
        else:
            return ''


def send_weather(update: Update, context: CallbackContext):
    response = get_weather(WEATHER_KEY, message=update.message.text)
    if int(response['cod']) == 200:

        city_name = response['name']
        temperature = response['main']['temp']
        feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        weekday = datetime.fromtimestamp(response['dt']).strftime(DATE_FORMAT)
        sunset = datetime.fromtimestamp(response['sys']['sunset']).strftime(TIME_FORMAT)
        sunrise = datetime.fromtimestamp(response['sys']['sunrise']).strftime(TIME_FORMAT)
        wind_deg = response['wind']['deg']
        wind_speed = response['wind']['speed']
        main_weather = response['weather'][0]['main']
        description = response['weather'][0]['description']
        emoji = get_emoji(main_weather)
        wind_direction = get_wind_direction(wind_deg) + str(wind_deg) + '°'

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Today {weekday} \nIn {city_name}: {description} {emoji}\n'
                                      f'🌡️ Temperature: {temperature}°C \n🌡️ Feels like: {feels_like}°C\n\n'
                                      f'💧 Humidity: {humidity}% \n🌅 Sunrise at {sunrise} \n🌇 Sunset at {sunset}\n'
                                      f'💨 Wind speed: {wind_speed} m/s \n🧭 Wind direction: {wind_direction}')
    else:
        error_message = response['message']
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
    return ConversationHandler.END
