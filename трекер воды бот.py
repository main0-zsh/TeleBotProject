import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from tokens import tracker_bot_token

scheduler = BackgroundScheduler()
scheduler.start()

water_ml=0
current_remind=None
remind1=0
remind2=1

bot=telebot.TeleBot(tracker_bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,'Привет! Я бот-трекер, который будет напоминать и проверять сколько воды ты выпил!\n/help-Полный туториал по этому боту')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id,'/setreminder1-Создать напоминалку, которая будет напоминать выпить воды каждый час\n/setreminder2-Создать напоминалку, которая будет напоминать выпить воды каждые 2 часа\n/drank_300-Добавляет 300 мл воды на общий баланс воды\n/status-Показывает информацию о тебе и твой статистику воды\n/stop_remind-Удалить напоминание')

def send_remind(chat_id, text):
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['setreminder1'])
def reminder1(message):
    global current_remind
    global remind1
    if current_remind is None:
        current_remind=remind1
        job_id = f'remind_{message.chat.id}'
        scheduler.add_job(
            func=send_remind,
            trigger='interval',
            hours=1,
            args=[message.chat.id, 'Вы должны попить 300 мл воды'],
            id=job_id,
            replace_existing=True
        )
        bot.send_message(message.chat.id, "Напоминание установлено!")
    else:
        bot.send_message(message.chat.id,'У вас уже есть активное напоминание! Удалите его, чтобы добавить этот')

@bot.message_handler(commands=['setreminder2'])
def reminder2(message):
    global current_remind
    global remind2
    if current_remind is None:
        current_remind=remind2
        job_id = f'remind_{message.chat.id}'
        scheduler.add_job(
            func=send_remind,
            trigger='interval',
            hours=2,
            args=[message.chat.id, 'Вы должны попить 300 мл воды'],
            id=job_id,
            replace_existing=True
        )
        bot.send_message(message.chat.id, "Напоминание установлено!")
    else:
        bot.send_message(message.chat.id,'У вас уже есть активное напоминание! Удалите его, чтобы добавить этот')

@bot.message_handler(commands=['drank_300'])
def drank_func(message):
    global water_ml
    water_ml+=300
    bot.send_message(message.chat.id,f'Вы пополнили свой баланс воды на 300 мл! Ваш общий баланс воды:{water_ml}')

@bot.message_handler(commands=['status'])
def send_status(message):
    global water_ml
    bot.send_message(message.chat.id,f'Ваша общая сумма выпитой воды:{water_ml}')

@bot.message_handler(commands=['stop_remind'])
def remove_remind(message):
    global current_remind
    job_id = f'remind_{message.chat.id}'
    try:
        scheduler.remove_job(job_id)
        current_remind=None
        bot.send_message(message.chat.id,'Вы удалили напоминание!')
    except:
        bot.send_message(message.chat.id,'У вас нет активных напоминаний')

bot.polling()