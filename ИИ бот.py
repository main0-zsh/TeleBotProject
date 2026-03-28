import telebot
from google import genai
from google.genai import types
from tokens import AI_bot_token, ai_api_key

# Твой токен и клиент
bot = telebot.TeleBot(AI_bot_token)
client = genai.Client(api_key=ai_api_key)

# ИСПРАВЛЕННОЕ НАЗВАНИЕ МОДЕЛИ
model = "models/gemini-1.5-flash"

AI_PERSONALITY = """Ты — Telegram-бот, обучающий программированию. Используй молодежный сленг..."""

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Йо! Я твой сленговый ментор. 👨‍💻 Пиши вопросы по коду, и я зачекаю их!")

@bot.message_handler(commands=['help'])
def help_message(message):
    # Теперь без запроса к ИИ — экономим лимиты!
    help_text = "База по командам:\n/start — го общаться\n/help — чекай команды\n/debug — разбор твоего кода\n/new_info — новые фишки"
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['debug', 'new_info'])
def ai_commands(message):
    try:
        config = types.GenerateContentConfig(system_instruction=AI_PERSONALITY)
        response = client.models.generate_content(
            model=model,
            contents=message.text,
            config=config
        )
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Бро, я притомился. Дай мне минуту! 🪫")

@bot.message_handler(content_types=['text'])
def reply_ai(message):
    try:
        config = types.GenerateContentConfig(system_instruction=AI_PERSONALITY)
        response = client.models.generate_content(
            model=model,
            contents=message.text,
            config=config
        )
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        if "429" in str(e):
            bot.send_message(message.chat.id, "Лимит запросов исчерпан. Зачекай позже! ⏳")
        else:
            print(f"Ошибка: {e}")

bot.polling()