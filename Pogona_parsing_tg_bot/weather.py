import json
import re

import requests
from bs4 import BeautifulSoup

import keyboards as kb

with open("city_catalog.json", 'r', encoding='utf-8') as file:
    json_load = json.load(file)


def get_month(city):
    try:
        url = "https://www.gismeteo.ru" + str(json_load[city]) + "month"
    except:
        url = ''
        return -1
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
        response2.append(
            "<b>" + (str(date + '\n' if len(date.split()) > 1 else date + str(' ' + cur_month + '\n'))) + "</b>")
        response2[
            -1] += f"{kb.pogoda_stikers[kb.pogoda_picture_num.index(pic_num)]} <u>{kb.pogoda_phrase[kb.pogoda_picture_num.index(pic_num)]}</u>  \n"
        # print(date if len(date.split()) > 1 else date + str(' ' + cur_month), end=' ')
        response2[-1] += f"минимальная температура: {mint} \nмаксимальная температура: {maxt} \n {pic_num}"
        # print("минимальная температура: ", mint, "      максимальная температура: ", maxt)

    return response2


def get_2week(city):
    try:
        url = "https://www.gismeteo.ru" + str(json_load[city]) + "2-weeks"
    except:
        url = ''
        return -1

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
    soup = BeautifulSoup(response.text, "lxml", parser='html.parser')
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

                try:
                    t_air.append([el.find(class_="maxt").find(class_="unit unit_temperature_c").text])
                except:
                    t_air.append(["-"])
                try:
                    t_air[-1].append(el.find(class_="mint").find(class_="unit unit_temperature_c").text)
                except:
                    t_air[-1].append("-")


        elif i.get("data-row") == "temperature-heat-index":
            for el in i.find_all(class_="value style_size_m"):
                try:
                    t_feel_air.append([el.find(class_="maxt").find(class_="unit unit_temperature_c").text])
                except:
                    t_feel_air.append(["-"])
                try:
                    t_feel_air[-1].append(el.find(class_="mint").find(class_="unit unit_temperature_c").text)
                except:
                    t_feel_air[-1].append("-")


        elif i.get("data-row") == "temperature-avg":
            for el in i.find(class_="values").find_all(class_="unit unit_temperature_c"):
                try:
                    t_avg_air.append(el.text)
                except:
                    t_avg_air.append("-")

    for el in all_wraps.find("div", {"data-row": "wind-speed"}).find_all(class_="row-item"):
        try:
            wind_avg_speed.append(el.find(class_="wind-unit unit unit_wind_m_s").text)
        except:
            wind_avg_speed.append("-")

    for el in all_wraps.find("div", {"data-row": "wind-gust"}).find_all(class_="row-item"):
        try:
            wind_gust.append(el.find(class_="wind-unit unit unit_wind_m_s").text)
        except:
            wind_gust.append("-")

    for el in all_wraps.find(class_="widget-row widget-row-precipitation-bars row-with-caption").find_all(
            class_="row-item"):
        try:
            precipitation.append(el.find(class_='item-unit').text)
        except:
            precipitation.append("-")

    for el in all_wraps.find(class_="widget-row-chart widget-row-chart-pressure row-with-caption").find_all(
            class_="value style_size_m"):
        try:
            pressure.append([el.find(class_="mint").find(class_="unit unit_pressure_mm_hg_atm").text])
        except:
            pressure.append(["-"])
        try:
            pressure[-1].append(el.find(class_="maxt").find(class_="unit unit_pressure_mm_hg_atm").text)
        except:
            pressure[-1].append("-")

    for el in all_wraps.find(class_="widget-row widget-row-wind-direction row-with-caption").find_all(
            class_="row-item"):
        try:
            wind_direction.append([str(el.next.get("class")[-1][-1]), str(el.find(class_="direction").text)])
        except:
            wind_direction.append(["-", "-"])

    for el in all_wraps.find(class_="widget-row widget-row-humidity row-with-caption").find_all(
            class_=re.compile("row-item")):
        try:
            humidity.append(el.text)
        except:
            humidity.append("-")

    for i in range(14):
        response2.append("<b>" + (all_dates[i]) + "</b>" + "\n")
        response2[-1] += kb.slash
        response2[-1] += (
                kb.pogoda_stikers[kb.pogoda_picture_num.index(all_icon_phrases[i])] + " <u>" + kb.pogoda_phrase[
            kb.pogoda_picture_num.index(all_icon_phrases[i])] + "</u>" + " \n")
        response2[-1] += kb.slash
        response2[-1] += ("🌡️ Ощущается как " + t_feel_air[i][1] + " ℃  -  " + t_feel_air[i][0] + " ℃ \n ")
        response2[-1] += ("🌡️ В среднем " + t_avg_air[i] + " ℃ \n")
        response2[-1] += kb.slash
        response2[-1] += ("🌬 Направление ветра " + kb.arrows_directions[
            kb.arrows_directions_alp.index(wind_direction[i][1])] + " " + wind_direction[i][1] + " \n")
        response2[-1] += ("🌬 Средняя скорость ветра " + wind_avg_speed[i] + "м/c \n")
        response2[-1] += kb.slash
        response2[-1] += ("💧 Относительная влажность " + humidity[i] + " % \n")
        response2[-1] += kb.slash
        response2[-1] += ("🎚️ Давление " + pressure[i][0] + " мм. рт. ст. \n ")
        response2[-1] += kb.slash
        response2[-1] += ("☔ Осадки " + precipitation[i] + " мм")
    return response2


def get_now(city):
    try:
        url = "https://www.gismeteo.ru" + json_load[city] + "now"
    except:
        url = ''
        return -1
    response2 = []
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    soup = BeautifulSoup(response.text, "lxml", parser='html.parser')
    main_wrap = soup.find(class_="section section-content section-bottom-shadow")
    day, data, time = main_wrap.find(class_="now-localdate").text.split(',')
    sunrise = main_wrap.find(class_="now-astro-sunrise").find(class_="time").text
    sunset = main_wrap.find(class_="now-astro-sunset").find(class_="time").text
    temp = main_wrap.find(class_="now-weather").find(class_="unit unit_temperature_c").text
    temp_feel = main_wrap.find(class_="now-feel").find(class_="unit unit_temperature_c").text
    desc = main_wrap.find(class_="now-desc").text
    main_states = [i.next.text for i in
                   main_wrap.find(class_="info-wrap").find_all(class_="item-value")]
    for i in range(len(main_states)):
        tmp = ''
        for j in range(len(main_states[i])):
            if (str(main_states[i][j]).isdigit() or main_states[i][j] in "+-"):
                tmp += main_states[i][j]
        main_states[i] = tmp

    response2.append(f"📅 <b>{data}, {day} {time} </b>{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🌡️ {temp}, ощущается как {temp_feel}️{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🌇 Восход {sunrise}   ⤼   🌄 Закат {sunset}{kb.nl} ")
    response2[-1] += kb.slash
    response2[-1] += (f"🌪️ Ветер {main_states[0]} м/с{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🎚️ Давление {main_states[1]} мм рт.ст.{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"💧 Относительная влажность {main_states[2]} %{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🧲 Г/м активность {main_states[3]} балла из 9{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🌊 Вода {main_states[4]} °C {kb.nl}")
    return response2[0]
