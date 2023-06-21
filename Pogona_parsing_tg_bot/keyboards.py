from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки городов
cities = ['Москва', 'Санкт-Петербург', 'Нижний Новгород', 'Казань']
nums = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
city_buttons = []
for i in range(4):
    city_buttons.append(KeyboardButton(nums[i] + cities[i]))

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
