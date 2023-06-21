from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки городов
city_button_Moscow = KeyboardButton('1️⃣  ️Москва')
city_button_Sant_Peter = KeyboardButton('2️⃣ Санкт Петербург')
city_button_Nijniy_Novgorod = KeyboardButton('️4️⃣ Нижний Новгород')
city_button_Kazan = KeyboardButton('3️⃣ Казань')

# кнопки погоды
weather_period_month = KeyboardButton("Месяц")
weather_period_toay = KeyboardButton("сегодня")
weather_period_3day = KeyboardButton("3 дня")
weather_period_week = KeyboardButton("Неделя")
weather_period_tomorrow = KeyboardButton("завтра")

# кнопки диалога
talk_start_1 = KeyboardButton('Погода, серьезно?')

# создание отдельных виртуальных клавиатур
markup_cities = ReplyKeyboardMarkup(resize_keyboard=True).row(city_button_Moscow, city_button_Sant_Peter).row(
    city_button_Kazan, city_button_Nijniy_Novgorod)
markup_talk_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(talk_start_1)
