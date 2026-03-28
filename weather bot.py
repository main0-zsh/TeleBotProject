import telebot
from telebot import types
import requests
from telebot.types import ReplyKeyboardMarkup
from tokens import weather_bot_key,weather_api_key


days=3

bot=telebot.TeleBot(weather_bot_key)

def get_weather_for_one_day(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no&lang=ru"
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        city_name=data['location']['name']
        temp=data['current']['temp_c']
        condition=data['current']['condition']['text']
        humidity=data['current']['humidity']
        wind_speed=data['current']['wind_kph']
        return f'Погода в городе {city_name}\nТемпература:{temp} С\nСостояние:{condition}\nВлажность:{humidity}%\nСкорость ветра:{wind_speed} км/час'
    else:
        return 'Ошибка. Не удалось найти данные о погоде.\nПроверьте правильность названия города'
def get_weather_for_few_days(city):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&days={days}&aqi=no&lang=ru"
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        forecast_list=data['forecast']['forecastday']
        report=f'Прогноз погоды в городе {city} на {days} дня'
        for day in forecast_list:
            date = day['date']
            max_temp=day['day']['maxtemp_c']
            min_temp=day['day']['mintemp_c']
            condition=day['day']['condition']['text']

            report+=f'\nДаты:{date}\nМаксимальная температура:{max_temp}\nМинимальная температура{min_temp}\nСостояние:{condition}'
    else:
        report='Ошибка. Проверьте правильность названия города.'
    return report

choice_markup=ReplyKeyboardMarkup(resize_keyboard=True)
weather_btn1=types.KeyboardButton('Погода на сегодня')
weather_btn2=types.KeyboardButton('Погода на несколько дней')

choice_markup.add(weather_btn1, weather_btn2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,'Привет! Я бот для погоды. Напиши свой город на английском и я скажу его погоду на данный момент\n/help-Все команды', reply_markup=choice_markup)
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '/start-Начало программы')

city_markup=ReplyKeyboardMarkup(resize_keyboard=True)
city_btn1=types.KeyboardButton('Moscow')
city_btn2=types.KeyboardButton('New York')
city_btn3=types.KeyboardButton('Paris')
city_btn4=types.KeyboardButton('Dubai')
city_btn5=types.KeyboardButton('Astana')
city_markup.add(city_btn1,city_btn2,city_btn3,city_btn4,city_btn5)

@bot.message_handler(content_types=['text'])
def analyze_message(message):
    if message.text=='Погода на сегодня':
        bot.send_message(message.chat.id,'Выбери один из этих городов или напиши название существующего города на английском',reply_markup=city_markup)
        bot.register_next_step_handler(message, weather_for_one_day)
    elif message.text=='Погода на несколько дней':
        bot.send_message(message.chat.id,'Выбери один из этих городов или напиши название существующего города на английском',reply_markup=city_markup)
        bot.register_next_step_handler(message, weather_for_three_days)

def weather_for_one_day(message):
    city = message.text
    report1 = get_weather_for_one_day(city)
    bot.reply_to(message, report1)

def weather_for_three_days(message):
    city=message.text
    report3=get_weather_for_few_days(city)
    bot.reply_to(message, report3)

bot.polling()