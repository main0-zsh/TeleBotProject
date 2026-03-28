import telebot
import requests
from telebot import types
from tokens import bot_token_currency1, api_key_currency1

bot_token=bot_token_currency1
api_key=api_key_currency1

currencies = ['KZT', 'RUB', 'CNY', 'USD', 'EUR', 'AED', 'GBP', 'JPY']

strings = {
    'ru': {
        'start': 'Привет! Я бот для конвертации. Введите сумму, которую хотите перевести:',
        'select_base': 'Выберите исходную валюту:',
        'select_target': 'Введите валюту, в которую хотите конвертировать:',
        'error_amount': 'Пожалуйста, введите число (сумму).',
        'error_currency': 'Ошибка. Выберите валюту из списка.',
        'error_api': 'Ошибка API или неверная валюта.',
        'help': 'Введите сумму (число), затем следуйте подсказкам кнопок.'
    },
    'en': {
        'start': 'Hello! I am a currency bot. Enter the amount you want to convert:',
        'select_base': 'Select base currency:',
        'select_target': 'Enter the currency you want to convert to:',
        'error_amount': 'Please enter a number (amount).',
        'error_currency': 'Error. Select a currency from the list.',
        'error_api': 'API error or invalid currency.',
        'help': 'Enter the amount (number), then follow the button prompts.'
    }
}

user_languages = {}

bot = telebot.TeleBot(bot_token)


def get_exchange_rate(base_currency, target_currency):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and target_currency in data['conversion_rates']:
            return data['conversion_rates'][target_currency]
        return None
    except:
        return None


def get_buttons():
    currency_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(curr) for curr in currencies]
    currency_markup.add(*buttons)
    return currency_markup


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Русский 🇷🇺', 'English 🇺🇸')
    bot.send_message(message.chat.id, "Выберите язык / Choose language:", reply_markup=markup)
    bot.register_next_step_handler(message, set_language)


def set_language(message):
    chat_id = message.chat.id
    if 'Русский' in message.text:
        user_languages[chat_id] = 'ru'
    else:
        user_languages[chat_id] = 'en'

    lang = user_languages[chat_id]
    bot.send_message(chat_id, strings[lang]['start'], reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['help'])
def help_message(message):
    lang = user_languages.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, strings[lang]['help'])


@bot.message_handler(content_types=['text'])
def convert_init(message):
    lang = user_languages.get(message.chat.id, 'ru')
    try:
        amount = float(message.text.replace(',', '.'))
        bot.send_message(message.chat.id, strings[lang]['select_base'], reply_markup=get_buttons())
        bot.register_next_step_handler(message, analyze_base_currency, amount, lang)
    except ValueError:
        bot.send_message(message.chat.id, strings[lang]['error_amount'])


def analyze_base_currency(message, amount, lang):
    base_currency = message.text.upper()
    if base_currency in currencies:
        bot.send_message(message.chat.id, strings[lang]['select_target'], reply_markup=get_buttons())
        bot.register_next_step_handler(message, final_exchange, base_currency, amount, lang)
    else:
        bot.send_message(message.chat.id, strings[lang]['error_currency'])


def final_exchange(message, base_currency, amount, lang):
    target_currency = message.text.upper()
    rate = get_exchange_rate(base_currency, target_currency)

    if rate:
        converted_amount = round(amount * rate, 2)
        bot.send_message(message.chat.id, f'✅ {amount} {base_currency} = {converted_amount} {target_currency}')
    else:
        bot.send_message(message.chat.id, strings[lang]['error_api'])


if __name__ == "__main__":
    bot.polling(none_stop=True)