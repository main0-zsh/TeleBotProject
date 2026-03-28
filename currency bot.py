import telebot
import requests
from tokens import bot_token_currency1, api_key_currency1

bot_token=bot_token_currency1
api_key=api_key_currency1

bot=telebot.TeleBot(bot_token)

def get_exchange_rate(base_currency,target_currency):
    url=f'https://v6.exchangerate-api.com/v6/295f00f171ae5b4823ce8429/latest/{base_currency}'
    response=requests.get(url)
    data=response.json()
    if response.status_code==200 and target_currency in data['conversion_rates']:
        return data['conversion_rates'][target_currency]
    else:
        return None

@bot.message_handler(commands=['start'])
def exchange_rate(message):
    bot.send_message(message.chat.id,'Привет, дружище! Я бот для конвертаций валют, готов помочь вам в любую секунду\n/help-Помощь с вводом валюты')

@bot.message_handler(commands=['help'])
def help_function(message):
    bot.send_message(message.chat.id,'Ты обязательно должен ввести 3 слова капсом: Сумму,Валюта1,Валюта2\nНапример:200 USD KZT\nВалюта1-Валюта,которую хочешь превартаить\nВалюта2-Валюта, которую хочешь получить')

@bot.message_handler(content_types=['text'])
def convert_currency(message):
    try:
        amount,base_currency,target_currency=message.text.split()
        rate=get_exchange_rate(base_currency,target_currency)
        if rate:
            converted_amount=float(amount)*rate
            bot.send_message(message.chat.id,f'{amount} {base_currency} в {target_currency}={converted_amount} {target_currency}')
        else:
            bot.reply_to(message, 'Ошибка. Такой валюты не существует.')
    except Exception as e:
        bot.reply_to(message,f'Ошибка:{e}. Проверьте правильность ввода')


bot.polling()
