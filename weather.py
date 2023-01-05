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
    'clear sky': '☀',
    'few clouds': '🌤',
    'scattered clouds': '⛅',
    'broken clouds': '🌥',
    'shower rain': '🌧',
    'rain': '🌧',
    'thunderstorm': '⛈',
    'mist': '🌫',
    'snow': '❄',
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
        description = response['weather'][0]['description']

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Today {weekday} \nIn {city_name}: {description}\n'
                                      f'🌡️ Temperature: {temperature}°C \n🌡️ Feels like: {feels_like}°C\n'
                                      f'💧 Humidity: {humidity}% \n🌅 Sunrise at {sunrise} \n🌇 Sunset at {sunset}')
    else:
        error_message = response['message']
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
    return ConversationHandler.END
