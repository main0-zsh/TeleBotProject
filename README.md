# TeleBotProject 🤖

Коллекция из 6 Telegram-ботов, написанных на Python с использованием библиотеки **pyTelegramBotAPI (telebot)**. Проект демонстрирует путь от простых эхо-ботов до интеграции с внешними API и искусственным интеллектом.

## 📁 Состав проекта

### 1. Currency Converter (v1)
Базовый конвертер валют. Обрабатывает текстовые запросы пользователя и пересчитывает суммы по заданному курсу.

### 2. Advanced Currency Converter (v2)
Улучшенная версия: более гибкий выбор валют и использование актуальных данных.

### 3. Weather Bot ☁️
Бот для получения прогноза погоды. Работает через внешнее API (OpenWeatherMap), парсит JSON-ответы и выводит температуру и состояние неба в красивом виде.

### 4. Gemini AI Bot ✨
Самый продвинутый бот в коллекции. Интегрирован с **Google Gemini AI**, что позволяет ему отвечать на вопросы, генерировать идеи и поддерживать осмысленный диалог.

### 5. Water Tracker 💧
Персональный помощник для контроля здоровья. Позволяет записывать количество выпитой воды за день и следить за прогрессом.

### 6. Command & UI Bot 🔘
Бот-демонстрация возможностей интерфейса: работа с `ReplyKeyboardMarkup` и `InlineKeyboardMarkup`, обработка различных типов контента и кнопок.

## 🛠 Технологии
* **Python 3**
* **pyTelegramBotAPI** (библиотека `telebot`)
* **Requests** (для сетевых запросов к API)
* **Google Generative AI** (библиотека для работы с Gemini)

## 🚀 Как запустить

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/main0-zsh/TeleBotProject.git](https://github.com/main0-zsh/TeleBotProject.git)
   cd TeleBotProject
Настройте ключи доступа:
Создайте файл tokens.py (он добавлен в .gitignore и не попадет в сеть) и пропишите там ваши API-ключи:

Python
# Пример содержания tokens.py
BOT_TOKEN = "ваш_токен_от_BotFather"
GEMINI_KEY = "ваш_ключ_от_Google_AI"
WEATHER_API_KEY = "ваш_ключ_погоды"
Установите зависимости:

Bash
./.venv/bin/python3 -m pip install pyTelegramBotAPI requests google-generativeai
Запуск любого бота:

Bash
./.venv/bin/python3 имя_файла_бота.py

📝 Автор

Разработано на Linux Mint. Проект создан для практики работы с API и логикой ботов на языке Python.
