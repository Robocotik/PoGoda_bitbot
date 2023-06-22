from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки городов
cities = ['Москва', 'Санкт-Петербург', 'Нижний Новгород', 'Казань']
nums_stikers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
pogoda_stikers = [
    "☀️",  # 1
    "🌤️",  # 2
    "🌦️",  # 3
    "🌦️",  # 4
    "⛅",  # 5
    "🌦️",  # 6
    "⛈",  # 7
    "🌦️",  # 8
    "⛈️",  # 9
    "⛈️",  # 10
    '☁️',  # 11
    '🌧️',  # 12
    '🌧️',  # 13
    '⛈️'  # 14
]
pogoda_phrase = [
    "Солнечно",  # 1
    "Малооблачно, без осадков",  # 2
    "Малооблачно, слабый дождь",  # 3
    "Малооблачно, сильный дождь",  # 4
    "Облачно, без осадков",  # 5
    "Пасмурно, слабый дождь",  # 6
    "Пасмурно, слабый дождь, гроза",  # 7
    "Облачно, сильный дождь",  # 8
    "Облачно, сильный дождь, гроза",  # 9
    "Облачно, сильный дождь, гроза",  # 10
    "Пасмурно, без осадков",  # 11
    "Пасмурно, слабый дождь",  # 12
    "Пасмурно, сильный дождь",  # 13
    "Пасмурно, сильный дождь, гроза"]  # 14
pogoda_picture_num = [
    "#d",  # 1
    "#d_c1",  # 2
    "#d_c1_r1",  # 3
    "#d_c1_r2",  # 4
    "#d_c2",  # 5
    "#d_c2_r1",  # 6
    "#d_c2_r1_st",  # 7
    "#d_c2_r2",  # 8
    "#d_c2_r2_st",  # 9
    "#d_c2_r3_st",  # 10
    "#d_c3",  # 11
    "#d_c3_r1",  # 12
    "#d_c3_r2",  # 13
    "#d_c3_r2_st"  # 14
]
city_buttons = []

for i in range(4):
    city_buttons.append(KeyboardButton(nums_stikers[i] + cities[i]))

# кнопки погоды
weather_periods = ['На вчера', 'На сегодня', 'На завтра', 'На 3 дня', 'На неделю', 'На месяц']

# кнопки диалога
talk_start_1 = KeyboardButton('Погода, серьезно?')

# создание отдельных виртуальных клавиатур
markup_cities = ReplyKeyboardMarkup(resize_keyboard=True).row(city_buttons[0], city_buttons[1]).row(
    city_buttons[2], city_buttons[3])
markup_talk_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(talk_start_1)
markup_weather_period = ReplyKeyboardMarkup(resize_keyboard=True).row(weather_periods[0], weather_periods[1],
                                                                      weather_periods[2]).row(weather_periods[3],
                                                                                              weather_periods[4],
                                                                                              weather_periods[5])
