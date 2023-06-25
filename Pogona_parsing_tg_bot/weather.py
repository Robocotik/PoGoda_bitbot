import json
import re

import requests
from aiogram.utils.markdown import bold
from bs4 import BeautifulSoup

import keyboards as kb

with open("city_catalog.json", 'r', encoding='utf-8') as file:
    json_load = json.load(file)


def get_month(city):
    url = "https://www.gismeteo.ru" + str(json_load[city]) + "month"
    print(url)
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    soup = BeautifulSoup(response.text, "lxml")
    response2 = []
    all_wraps = soup.find("div", class_="widget widget-month").find_all(class_="row-item")
    cur_month = ''
    for wrap in all_wraps:
        mint = wrap.find(class_="mint").find(class_="unit unit_temperature_c").text
        maxt = wrap.find(class_="maxt").find(class_="unit unit_temperature_c").text
        date = wrap.find(class_="date").text
        pic_num = wrap.find("use").get("xlink:href")

        if len(date.split()) > 1:
            cur_month = date.split()[-1]
        response2.append(kb.pogoda_stikers[kb.pogoda_picture_num.index(pic_num)] + " " + kb.pogoda_phrase[
            kb.pogoda_picture_num.index(pic_num)] + "\n")
        response2[-1] += (str(date + '\n' if len(date.split()) > 1 else date + str(' ' + cur_month + '\n')))
        # print(date if len(date.split()) > 1 else date + str(' ' + cur_month), end=' ')
        response2[-1] += "минимальная температура: " + str(mint) + "\n" + "максимальная температура: " + str(
            maxt) + "\n" + str(pic_num)
        # print("минимальная температура: ", mint, "      максимальная температура: ", maxt)

    return response2


def get_2week(city):
    url = "https://www.gismeteo.ru" + str(json_load[city]) + "2-weeks"
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    t_air = []
    t_feel_air = []
    t_avg_air = []
    wind_avg_speed = []
    wind_gust = []
    wind_direction = []
    precipitation = []
    pressure = []
    humidity = []
    response2 = []
    soup = BeautifulSoup(response.text, "lxml")
    all_wraps = soup.find("div", class_="widget-body widget-columns-14").find(class_="widget-items")
    all_dates = [i.text for i in all_wraps.find(class_="widget-row widget-row-days-date").find_all(class_="date")]
    cur_month = ''
    for i in range(len(all_dates)):
        if len(all_dates[i].split()) > 1:
            cur_month = all_dates[i].split()[-1]
        else:
            all_dates[i] += ' ' + cur_month

    all_icon_phrases = [i.find("use").get("href") for i in
                        all_wraps.find(class_="widget-row widget-row-icon").find_all(class_="row-item")]

    for i in all_wraps.find_all("div", class_="widget-row-chart widget-row-chart-temperature row-with-caption"):
        if i.get("data-row") == "temperature-air":
            for el in i.find_all(class_="value style_size_m"):
                t_air.append([el.find(class_="maxt").find(class_="unit unit_temperature_c").text,
                              el.find(class_="mint").find(class_="unit unit_temperature_c").text])
        elif i.get("data-row") == "temperature-heat-index":
            for el in i.find_all(class_="value style_size_m"):
                t_feel_air.append([el.find(class_="maxt").find(class_="unit unit_temperature_c").text,
                                   el.find(class_="mint").find(class_="unit unit_temperature_c").text])
        elif i.get("data-row") == "temperature-avg":
            for el in i.find(class_="values").find_all(class_="unit unit_temperature_c"):
                t_avg_air.append(el.text)

    for el in all_wraps.find("div", {"data-row": "wind-speed"}).find_all(class_="row-item"):
        wind_avg_speed.append(el.find(class_="wind-unit unit unit_wind_m_s").text)

    for el in all_wraps.find("div", {"data-row": "wind-gust"}).find_all(class_="row-item"):
        wind_gust.append(el.find(class_="wind-unit unit unit_wind_m_s").text)

    for el in all_wraps.find(class_="widget-row widget-row-precipitation-bars row-with-caption").find_all(
            class_="row-item"):
        precipitation.append(el.find(class_='item-unit').text)

    for el in all_wraps.find(class_="widget-row-chart widget-row-chart-pressure row-with-caption").find_all(
            class_="value style_size_m"):
        pressure.append([])
        try:
            pressure[-1].append(el.find(class_="mint").find(class_="unit unit_pressure_mm_hg_atm").text)
        except:
            pressure[-1].append("-")
        try:
            pressure[-1].append(el.find(class_="maxt").find(class_="unit unit_pressure_mm_hg_atm").text)
        except:
            pressure[-1].append("-")

    for el in all_wraps.find(class_="widget-row widget-row-wind-direction row-with-caption").find_all(
            class_="row-item"):
        wind_direction.append([str(el.next.get("class")[-1][-1]), str(el.find(class_="direction").text)])

    for el in all_wraps.find(class_="widget-row widget-row-humidity row-with-caption").find_all(
            class_=re.compile("row-item")):
        humidity.append(el.text)
    print(humidity)
    for i in range(14):
        response2.append(bold(all_dates[i]) + "\n")
        response2[-1] += "-------------------------------------- \n"
        response2[-1] += (
                kb.pogoda_stikers[kb.pogoda_picture_num.index(all_icon_phrases[i])] + " " + kb.pogoda_phrase[
            kb.pogoda_picture_num.index(all_icon_phrases[i])] + " \n ")
        response2[-1] += "-------------------------------------- \n"
        response2[-1] += ("🌡️ Ощущается как " + t_feel_air[i][1] + " ℃  -  " + t_feel_air[i][0] + " ℃ \n ")
        response2[-1] += ("🌡️ В среднем " + t_avg_air[i] + " ℃ \n ")
        response2[-1] += "-------------------------------------- \n"
        response2[-1] += ("🌪️ Направление ветра " + kb.arrows_directions[
            kb.arrows_directions_alp.index(wind_direction[i][1])] + " " + wind_direction[i][1] + " \n ")
        response2[-1] += ("🌪️ Средняя скорость ветра " + wind_avg_speed[i] + "м/c \n ")
        response2[-1] += "-------------------------------------- \n"
        response2[-1] += ("💧 Относительная влажность " + humidity[i] + " % \n ")
        response2[-1] += "-------------------------------------- \n"
        response2[-1] += ("🎚️ Давление " + pressure[i][0] + " мм. рт. ст. \n ")
    return response2
