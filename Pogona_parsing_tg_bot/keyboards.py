from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def check_the_dick_for_key(dick, key_find):
    for key in dick:
        if key_find == key:
            return 1
    return 0


# кнопки городов
nums_stikers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
pogoda_stikers = [
    "☀️",  # 1
    "🌤️",  # 2
    "🌦️",  # 3
    "🌦️",  # 4
    "🌦️",  # 5
    "⛅",  # 6
    "🌦️",  # 7
    "⛈",  # 8
    "🌦️",  # 9
    "⛈️",  # 10
    "⛈️",  # 11
    '☁️',  # 12
    '🌧️',  # 13
    '🌧️',  # 14
    '🌧️',  # 15
    '⛈️'  # 15
]
pogoda_phrase = [
    "Солнечно",  # 1
    "Малооблачно, без осадков",  # 2
    "Малооблачно, слабый дождь",  # 3
    "Малооблачно, слабый дождь, гроза",  # 4
    "Малооблачно, сильный дождь",  # 5
    "Облачно, без осадков",  # 6
    "Пасмурно, слабый дождь",  # 7
    "Пасмурно, слабый дождь, гроза",  # 8
    "Облачно, сильный дождь",  # 9
    "Облачно, сильный дождь, гроза",  # 10
    "Облачно, сильный дождь, гроза",  # 11
    "Пасмурно, без осадков",  # 12
    "Пасмурно, слабый дождь",  # 13
    "Пасмурно, сильный дождь",  # 14
    "Пасмурно, сильный дождь",  # 15
    "Пасмурно, сильный дождь, гроза"]  # 16
pogoda_picture_num = [
    "#d",  # 1
    "#d_c1",  # 2
    "#d_c1_r1",  # 3
    "#d_c1_r1_st",  # 4
    "#d_c1_r2",  # 5
    "#d_c2",  # 6
    "#d_c2_r1",  # 7
    "#d_c2_r1_st",  # 8
    "#d_c2_r2",  # 9
    "#d_c2_r2_st",  # 10
    "#d_c2_r3_st",  # 11
    "#d_c3",  # 12
    "#d_c3_r1",  # 13
    "#d_c3_r2",  # 14
    "#d_c3_r3",  # 15
    "#d_c3_r2_st"  # 16
]

# кнопки погоды
weather_periods = ['На сейчас', 'На сегодня', 'На завтра', 'На 3 дня', 'На две недели', 'На месяц']

# кнопки диалога
talk_start_1 = KeyboardButton('/Погода,серьезно?')

# создание отдельных виртуальных клавиатур
markup_talk_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(talk_start_1)
markup_weather_period = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(weather_periods[0],
                                                                                              weather_periods[1],
                                                                                              weather_periods[2]).row(
    weather_periods[3],
    weather_periods[4],
    weather_periods[5])
