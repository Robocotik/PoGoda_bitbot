import json
import re

import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup

with open("city_catalog.json", 'r', encoding='utf-8') as file:
    json_load = json.load(file)
nl = '\n'


# часть парсинга
def find_10_day_periods(city):
    try:
        url = "https://www.gismeteo.ru" + json_load[city] + "3-days"
    except:
        url = ''
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    soup = BeautifulSoup(response.text, "lxml", parser='html.parser')
    all_wraps = soup.find("div", class_="widget widget-weather-parameters widget-threedays").find(class_="widget-items")
    all_days = [i.text for i in all_wraps.find(class_="widget-date-wrap").find_all(class_=re.compile("item"))]
    for i in range(len(all_days)):
        all_days[i] = nums_stikers[i] + " " + all_days[i] + nl
    print(all_days)
    return all_days


def check_the_dick_for_key(dick, key_find):
    for key in dick:
        if key_find == key:
            return 1
    return 0


# кнопки городов
nums_stikers = ["➊", "➋", "➌", "➍", "➎", "➏", "➐", "➑", "➒", "➓"]
slash = "--------------------------------------------------------- \n"

pogoda_stikers = [
    "☀️",  # 1
    "🌫️",  # 2

    "🌤️",  # 3
    "🌦️",  # 4
    "⛈️",  # 5
    "🌦️",  # 6
    "⛈️",  # 7
    "🌦️",  # 8
    "⛈️",  # 9
    "❄️🌧️❄️",  # 10
    "❄️⛈️❄️",  # 11
    '❄️🌧️❄️',  # 12
    '❄️⛈️❄️',  # 13
    '❄️🌧️❄️',  # 14
    '❄️⛈️❄️',  # 15
    '🌨️',  # 16

    "⚡🌨️⚡",  # 17
    "🌨️",  # 18
    "⚡🌨️⚡",  # 19
    "🌨️",  # 20
    "⚡🌨️⚡",  # 21
    "🌤️",  # 22
    "🌦️",  # 23
    "⛈️",  # 24
    "🌦️",  # 25
    "⛈️",  # 26
    "🌦️",  # 27
    '⛈️',  # 28
    '❄️🌧️❄️',  # 29
    '❄️⛈️❄️',  # 30
    '❄️🌧️❄️',  # 31
    '❄️⛈️❄️',  # 32

    "❄️🌧️❄️",  # 33
    "❄️⛈️❄️",  # 34
    "🌨️",  # 35
    "⚡🌨️⚡",  # 36
    "🌨️",  # 37
    "⚡🌨️⚡",  # 38
    "🌨️",  # 39
    "⚡🌨️⚡",  # 40
    "🌥️",  # 41
    "🌦️",  # 42
    "⛈️",  # 43
    '🌦️',  # 44
    '⛈️',  # 45
    '🌦️',  # 46
    '⛈️',  # 47
    '❄️🌧️❄️',  # 48

    "❄️⛈️❄️",  # 49
    "❄️🌧️❄️",  # 50
    "❄️⛈️❄️",  # 51
    "❄️🌧️❄️",  # 52
    "❄️⛈️❄️",  # 53
    "🌨️",  # 54
    "⚡🌨️⚡",  # 55
    "🌨️",  # 56
    "⚡🌨️⚡",  # 57
    "🌨️",  # 58
    "⚡🌨️⚡",  # 59
    '☁️',  # 60
    '🌧️',  # 61
    '⛈️',  # 62
    '🌧️',  # 63
    '⛈️',  # 64

    "🌧",  # 65
    "⛈️",  # 66
    "❄️🌧️❄️",  # 67
    "❄️⛈️❄️",  # 68
    "❄️🌧️❄️",  # 69
    "❄️⛈️❄️",  # 70
    "❄️🌧️❄️",  # 71
    "❄️⛈️❄️",  # 72
    "🌨️",  # 73
    "⚡🌨️⚡",  # 74
    "🌨️",  # 75
    '⚡🌨️⚡',  # 76
    '🌨️',  # 77
    '⚡🌨️⚡',  # 78

    "🌒",  # 1
    "🌒",  # 2

    "🌒",  # 3
    "🌒",  # 4
    "🌒",  # 5
    "🌒",  # 6
    "🌒",  # 7
    "🌒",  # 8
    "🌒",  # 9
    "🌒",  # 10
    "🌒",  # 11
    '🌒',  # 12
    '🌒',  # 13
    '🌒',  # 14
    '🌒',  # 15
    '🌒',  # 16

    "🌒",  # 17
    "🌒",  # 18
    "🌒",  # 19
    "🌒",  # 20
    "🌒",  # 21
    "🌒",  # 22
    "🌒",  # 23
    "🌒",  # 24
    "🌒",  # 25
    "🌒",  # 26
    "🌒",  # 27
    '🌒',  # 28
    '🌒',  # 29
    '🌒',  # 30
    '🌒',  # 31
    '🌒',  # 32

    "🌒",  # 33
    "🌒",  # 34
    "🌒",  # 35
    "🌒",  # 36
    "🌒",  # 37
    "🌒",  # 38
    "🌒",  # 39
    "🌒",  # 40
    "🌒",  # 41
    "🌒",  # 42
    "🌒",  # 43
    '🌒',  # 44
    '🌒',  # 45
    '🌒',  # 46
    '🌒',  # 47
    '🌒',  # 48

    "🌒",  # 49
    "🌒",  # 50
    "🌒",  # 51
    "🌒",  # 52
    "🌒",  # 53
    "🌒",  # 54
    "🌒",  # 55
    "🌒",  # 56
    "🌒",  # 57
    "🌒",  # 58
    "🌒",  # 59
    '🌒',  # 60
    '🌒',  # 61
    '🌒',  # 62
    '🌒',  # 63
    '🌒',  # 64

    "🌒",  # 65
    "🌒",  # 66
    "🌒",  # 67
    "🌒",  # 68
    "🌒",  # 69
    "🌒",  # 70
    "🌒",  # 71
    "🌒",  # 72
    "🌒",  # 73
    "🌒",  # 74
    "🌒",  # 75
    '🌒',  # 76
    '🌒',  # 77
    '🌒'  # 78
]
pogoda_phrase = [
    "Солнечно",  # 1
    "Туман",  # 2

    "Малооблачно, без осадков",  # 3
    "Малооблачно, слабый дождь",  # 4
    "Малооблачно, слабый дождь, гроза",  # 5
    "Малооблачно, дождь",  # 6
    "Малооблачно, дождь, гроза",  # 7
    "Малооблачно, сильный дождь",  # 8
    "Малооблачно, сильный дождь, гроза",  # 9
    "Малооблачно, слабый дождь и снег",  # 10
    "Малооблачно, слабый дождь и снег, гроза",  # 11
    "Малооблачно, дождь и снег",  # 12
    "Малооблачно, дождь и снег, гроза",  # 13
    "Малооблачно, сильный дождь и снег",  # 14
    "Малооблачно, сильный дождь и снег, гроза",  # 15
    "Малооблачно, слабый снег",  # 16
    "Малооблачно, слабый снег, гроза",  # 17
    "Малооблачно, снег",  # 18
    "Малооблачно, снег, гроза",  # 19
    "Малооблачно, сильный снег",  # 20
    "Малооблачно, сильный снег, гроза",  # 21

    "Малооблачно, без осадков",  # 22
    "Малооблачно, слабый дождь",  # 23
    "Малооблачно, слабый дождь, гроза",  # 24
    "Малооблачно, дождь",  # 25
    "Малооблачно, дождь, гроза",  # 26
    "Малооблачно, сильный дождь",  # 27
    "Малооблачно, сильный дождь, гроза",  # 28
    "Малооблачно, слабый дождь и снег",  # 29
    "Малооблачно, слабый дождь и снег, гроза",  # 30
    "Малооблачно, дождь и снег",  # 31
    "Малооблачно, дождь и снег, гроза",  # 32
    "Малооблачно, сильный дождь и снег",  # 33
    "Малооблачно, сильный дождь и снег, гроза",  # 34
    "Малооблачно, слабый снег",  # 35
    "Малооблачно, слабый снег, гроза",  # 36
    "Малооблачно, снег",  # 37
    "Малооблачно, снег, гроза",  # 38
    "Малооблачно, сильный снег",  # 39
    "Малооблачно, сильный снег, гроза",  # 40

    "Облачно, без осадков",  # 41
    "Облачно, слабый дождь",  # 42
    "Облачно, слабый дождь, гроза",  # 43
    "Облачно, дождь",  # 44
    "Облачно, дождь, гроза",  # 45
    "Облачно, сильный дождь",  # 46
    "Облачно, сильный дождь, гроза",  # 47
    "Облачно, слабый дождь и снег",  # 48
    "Облачно, слабый дождь и снег, гроза",  # 49
    "Облачно, дождь и снег",  # 50
    "Облачно, дождь и снег, гроза",  # 51
    "Облачно, сильный дождь и снег",  # 52
    "Облачно, сильный дождь и снег, гроза",  # 53
    "Облачно, слабый снег",  # 54
    "Облачно, слабый снег, гроза",  # 55
    "Облачно, снег",  # 56
    "Облачно, снег, гроза",  # 57
    "Облачно, сильный снег",  # 58
    "Облачно, сильный снег, гроза",  # 59

    "Пасмурно, без осадков",  # 60
    "Пасмурно, слабый дождь",  # 61
    "Пасмурно, слабый дождь, гроза",  # 62
    "Пасмурно, дождь",  # 63
    "Пасмурно, дождь, гроза",  # 64
    "Пасмурно, сильный дождь",  # 65
    "Пасмурно, сильный дождь, гроза",  # 66
    "Пасмурно, слабый дождь и снег",  # 67
    "Пасмурно, слабый дождь и снег, гроза",  # 68
    "Пасмурно, дождь и снег",  # 69
    "Пасмурно, дождь и снег, гроза",  # 70
    "Пасмурно, сильный дождь и снег",  # 71
    "Пасмурно, сильный дождь и снег, гроза",  # 72
    "Пасмурно, слабый снег",  # 73
    "Пасмурно, слабый снег, гроза",  # 74
    "Пасмурно, снег",  # 75
    "Пасмурно, снег, гроза",  # 76
    "Пасмурно, сильный снег",  # 77
    "Пасмурно, сильный снег, гроза",  # 78

    "Ночь, солнечно",  # 1
    "Ночь, туман",  # 2

    "Ночь, малооблачно, без осадков",  # 3
    "Ночь, малооблачно, слабый дождь",  # 4
    "Ночь, малооблачно, слабый дождь, гроза",  # 5
    "Ночь, малооблачно, дождь",  # 6
    "Ночь, малооблачно, дождь, гроза",  # 7
    "Ночь, малооблачно, сильный дождь",  # 8
    "Ночь, малооблачно, сильный дождь, гроза",  # 9
    "Ночь, малооблачно, слабый дождь и снег",  # 10
    "Ночь, малооблачно, слабый дождь и снег, гроза",  # 11
    "Ночь, малооблачно, дождь и снег",  # 12
    "Ночь, малооблачно, дождь и снег, гроза",  # 13
    "Ночь, малооблачно, сильный дождь и снег",  # 14
    "Ночь, малооблачно, сильный дождь и снег, гроза",  # 15
    "Ночь, малооблачно, слабый снег",  # 16
    "Ночь, малооблачно, слабый снег, гроза",  # 17
    "Ночь, малооблачно, снег",  # 18
    "Ночь, малооблачно, снег, гроза",  # 19
    "Ночь, малооблачно, сильный снег",  # 20
    "Ночь, малооблачно, сильный снег, гроза",  # 21

    "Ночь, малооблачно, без осадков",  # 22
    "Ночь, малооблачно, слабый дождь",  # 23
    "Ночь, малооблачно, слабый дождь, гроза",  # 24
    "Ночь, малооблачно, дождь",  # 25
    "Ночь, малооблачно, дождь, гроза",  # 26
    "Ночь, малооблачно, сильный дождь",  # 27
    "Ночь, малооблачно, сильный дождь, гроза",  # 28
    "Ночь, малооблачно, слабый дождь и снег",  # 29
    "Ночь, малооблачно, слабый дождь и снег, гроза",  # 30
    "Ночь, малооблачно, дождь и снег",  # 31
    "Ночь, малооблачно, дождь и снег, гроза",  # 32
    "Ночь, малооблачно, сильный дождь и снег",  # 33
    "Ночь, малооблачно, сильный дождь и снег, гроза",  # 34
    "Ночь, малооблачно, слабый снег",  # 35
    "Ночь, малооблачно, слабый снег, гроза",  # 36
    "Ночь, малооблачно, снег",  # 37
    "Ночь, малооблачно, снег, гроза",  # 38
    "Ночь, малооблачно, сильный снег",  # 39
    "Ночь, малооблачно, сильный снег, гроза",  # 40

    "Ночь, облачно, без осадков",  # 41
    "Ночь, облачно, слабый дождь",  # 42
    "Ночь, облачно, слабый дождь, гроза",  # 43
    "Ночь, облачно, дождь",  # 44
    "Ночь, облачно, дождь, гроза",  # 45
    "Ночь, облачно, сильный дождь",  # 46
    "Ночь, облачно, сильный дождь, гроза",  # 47
    "Ночь, облачно, слабый дождь и снег",  # 48
    "Ночь, облачно, слабый дождь и снег, гроза",  # 49
    "Ночь, облачно, дождь и снег",  # 50
    "Ночь, облачно, дождь и снег, гроза",  # 51
    "Ночь, облачно, сильный дождь и снег",  # 52
    "Ночь, облачно, сильный дождь и снег, гроза",  # 53
    "Ночь, облачно, слабый снег",  # 54
    "Ночь, облачно, слабый снег, гроза",  # 55
    "Ночь, облачно, снег",  # 56
    "Ночь, облачно, снег, гроза",  # 57
    "Ночь, облачно, сильный снег",  # 58
    "Ночь, облачно, сильный снег, гроза",  # 59

    "Ночь, пасмурно, без осадков",  # 60
    "Ночь, пасмурно, слабый дождь",  # 61
    "Ночь, пасмурно, слабый дождь, гроза",  # 62
    "Ночь, пасмурно, дождь",  # 63
    "Ночь, пасмурно, дождь, гроза",  # 64
    "Ночь, пасмурно, сильный дождь",  # 65
    "Ночь, пасмурно, сильный дождь, гроза",  # 66
    "Ночь, пасмурно, слабый дождь и снег",  # 67
    "Ночь, пасмурно, слабый дождь и снег, гроза",  # 68
    "Ночь, пасмурно, дождь и снег",  # 69
    "Ночь, пасмурно, дождь и снег, гроза",  # 70
    "Ночь, пасмурно, сильный дождь и снег",  # 71
    "Ночь, пасмурно, сильный дождь и снег, гроза",  # 72
    "Ночь, пасмурно, слабый снег",  # 73
    "Ночь, пасмурно, слабый снег, гроза",  # 74
    "Ночь, пасмурно, снег",  # 75
    "Ночь, пасмурно, снег, гроза",  # 76
    "Ночь, пасмурно, сильный снег",  # 77
    "Ночь, пасмурно, сильный снег, гроза"  # 78
]
pogoda_picture_num = [
    "#d",  # 1
    "#mist",  # 2

    "#d_c0",  # 3
    "#d_c0_r1",  # 4
    "#d_c0_r1_st",  # 5
    "#d_c0_r2",  # 6
    "#d_c0_r2_st",  # 7
    "#d_c0_r3",  # 8
    "#d_c0_r3_st",  # 9
    "#d_c0_rs1",  # 10
    "#d_c0_rs1_st",  # 11
    "#d_c0_rs2",  # 12
    "#d_c0_rs2_st",  # 13
    "#d_c0_rs3",  # 14
    "#d_c0_rs3_st",  # 15
    "#d_c0_s1",  # 16
    "#d_c0_s1_st",  # 17
    "#d_c0_s2",  # 18
    "#d_c0_s2_st",  # 19
    "#d_c0_s3",  # 20
    "#d_c0_s3_st",  # 21

    "#d_c1",  # 22
    "#d_c1_r1",  # 23
    "#d_c1_r1_st",  # 24
    "#d_c1_r2",  # 25
    "#d_c1_r2_st",  # 26
    "#d_c1_r3",  # 27
    "#d_c1_r3_st",  # 28
    "#d_c1_rs1",  # 29
    "#d_c1_rs1_st",  # 30
    "#d_c1_rs2",  # 31
    "#d_c1_rs2_st",  # 32
    "#d_c1_rs3",  # 33
    "#d_c1_rs3_st",  # 34
    "#d_c1_s1",  # 35
    "#d_c1_s1_st",  # 36
    "#d_c1_s2",  # 37
    "#d_c1_s2_st",  # 38
    "#d_c1_s3",  # 39
    "#d_c1_s3_st",  # 40

    "#d_c2",  # 41
    "#d_c2_r1",  # 42
    "#d_c2_r1_st",  # 43
    "#d_c2_r2",  # 44
    "#d_c2_r2_st",  # 45
    "#d_c2_r3",  # 46
    "#d_c2_r3_st",  # 47
    "#d_c2_rs1",  # 48
    "#d_c2_rs1_st",  # 49
    "#d_c2_rs2",  # 50
    "#d_c2_rs2_st",  # 51
    "#d_c2_rs3",  # 52
    "#d_c2_rs3_st",  # 53
    "#d_c2_s1",  # 54
    "#d_c2_s1_st",  # 55
    "#d_c2_s2",  # 56
    "#d_c2_s2_st",  # 57
    "#d_c2_s3",  # 58
    "#d_c2_s3_st",  # 59

    "#d_c3",  # 60
    "#d_c3_r1",  # 61
    "#d_c3_r1_st",  # 62
    "#d_c3_r2",  # 63
    "#d_c3_r2_st",  # 64
    "#d_c3_r3",  # 65
    "#d_c3_r3_st",  # 66
    "#d_c3_rs1",  # 67
    "#d_c3_rs1_st",  # 68
    "#d_c3_rs2",  # 69
    "#d_c3_rs2_st",  # 70
    "#d_c3_rs3",  # 71
    "#d_c3_rs3_st",  # 72
    "#d_c3_s1",  # 73
    "#d_c3_s1_st",  # 74
    "#d_c3_s2",  # 75
    "#d_c3_s2_st",  # 76
    "#d_c3_s3",  # 77
    "#d_c3_s3_st",  # 78

    "#n",  # 79
    "#n_mist",  # 80

    "#n_c0",  # 81
    "#n_c0_r1",  # 82
    "#n_c0_r1_st",  # 83
    "#n_c0_r2",  # 84
    "#n_c0_r2_st",  # 85
    "#n_c0_r3",  # 86
    "#n_c0_r3_st",  # 87
    "#n_c0_rs1",  # 88
    "#n_c0_rs1_st",  # 89
    "#n_c0_rs2",  # 90
    "#n_c0_rs2_st",  # 91
    "#n_c0_rs3",  # 92
    "#n_c0_rs3_st",  # 93
    "#n_c0_s1",  # 94
    "#n_c0_s1_st",  # 95
    "#n_c0_s2",  # 96
    "#n_c0_s2_st",  # 97
    "#n_c0_s3",  # 98
    "#n_c0_s3_st",  # 99

    "#n_c1",  # 100
    "#n_c1_r1",  # 101
    "#n_c1_r1_st",  # 102
    "#n_c1_r2",  # 103
    "#n_c1_r2_st",  # 104
    "#n_c1_r3",  # 105
    "#n_c1_r3_st",  # 106
    "#n_c1_rs1",  # 107
    "#n_c1_rs1_st",  # 108
    "#n_c1_rs2",  # 109
    "#n_c1_rs2_st",  # 110
    "#n_c1_rs3",  # 111
    "#n_c1_rs3_st",  # 112
    "#n_c1_s1",  # 113
    "#n_c1_s1_st",  # 114
    "#n_c1_s2",  # 115
    "#n_c1_s2_st",  # 116
    "#n_c1_s3",  # 117
    "#n_c1_s3_st",  # 118

    "#n_c2",  # 119
    "#n_c2_r1",  # 120
    "#n_c2_r1_st",  # 121
    "#n_c2_r2",  # 122
    "#n_c2_r2_st",  # 123
    "#n_c2_r3",  # 124
    "#n_c2_r3_st",  # 125
    "#n_c2_rs1",  # 126
    "#n_c2_rs1_st",  # 127
    "#n_c2_rs2",  # 128
    "#n_c2_rs2_st",  # 129
    "#n_c2_rs3",  # 130
    "#n_c2_rs3_st",  # 131
    "#n_c2_s1",  # 132
    "#n_c2_s1_st",  # 133
    "#n_c2_s2",  # 134
    "#n_c2_s2_st",  # 135
    "#n_c2_s3",  # 136
    "#n_c2_s3_st",  # 137

    "#n_c3",  # 138
    "#n_c3_r1",  # 139
    "#n_c3_r1_st",  # 140
    "#n_c3_r2",  # 141
    "#n_c3_r2_st",  # 142
    "#n_c3_r3",  # 143
    "#n_c3_r3_st",  # 144
    "#n_c3_rs1",  # 145
    "#n_c3_rs1_st",  # 146
    "#n_c3_rs2",  # 147
    "#n_c3_rs2_st",  # 148
    "#n_c3_rs3",  # 149
    "#n_c3_rs3_st",  # 150
    "#n_c3_s1",  # 151
    "#n_c3_s1_st",  # 152
    "#n_c3_s2",  # 153
    "#n_c3_s2_st",  # 154
    "#n_c3_s3",  # 155
    "#n_c3_s3_st"  # 156
]

arrows_directions = ["⬆️", "↗️", "➡️", "↘️", "⬇️", "↙️", "⬅️", "↖️", "⚪"]
arrows_directions_alp = ["Ю", "ЮЗ", "З", "СЗ", "С", "СВ", "В", "ЮВ", "штиль"]
# кнопки погоды
weather_periods = ['На сейчас', 'На ближайший день', 'На две недели', 'На месяц']
# кнопки диалога
talk_start_1 = KeyboardButton('Погода, серьезно?')

# создание отдельных виртуальных клавиатур
markup_retry = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton("Еще по-братски"),
                                                                                     KeyboardButton("Изменить город"))
markup_talk_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(talk_start_1)
markup_weather_period = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(weather_periods[0],
                                                                                              weather_periods[1]).row(
    weather_periods[2], weather_periods[3])
