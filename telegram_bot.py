import telebot
from telebot import types
from tokens import telegram_bot_token

token=telegram_bot_token
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Привет! Это новый бот Адиля\n/help-Все команды")

markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton('Кнопка 1')
item2=types.KeyboardButton('Ничего')
markup.add(item1)
markup.add(item2)

@bot.message_handler(commands=['button'])
def button_message(message):
    bot.send_message(message.chat.id,"Нажми на кнопку", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,"/start-Начать бота\n/button-Меню кнопок\n/send_sticker-Отправить стикер")

@bot.message_handler(commands=['send_sticker'])
def sticker_message(message):
    bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAM7aXYXVmQskjdT9fl-M1VZsE5h2yIAApWRAAITBohKQQj7JbJJZ3w4BA")

@bot.message_handler(content_types=['text'])
def reaction_button(message):
    if message.text=="Кнопка 1":
        bot.send_message(message.chat.id,"Вы нажали на кнопку")
    if message.text=='Ничего':
        bot.send_message(message.chat.id,"Зачем ты нажал на эту кнопку? Думал что тут будет что-то оссобенное?")
bot.polling()