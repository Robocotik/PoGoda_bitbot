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
            "<b><u>📅 " + (
                str(date + '\n' if len(date.split()) > 1 else date + str(' ' + cur_month + '\n'))) + "</u></b>")
        response2[-1] += kb.slash
        response2[
            -1] += f"{kb.pogoda_stikers[kb.pogoda_picture_num.index(pic_num)]} <b>{kb.pogoda_phrase[kb.pogoda_picture_num.index(pic_num)]}</b>  \n"
        response2[-1] += kb.slash

        response2[-1] += f"<b>🌡 мин температура </b> {mint} ℃ \n<b>🌡 макс температура </b> {maxt} ℃ \n {pic_num}"


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
    all_days = [i.text for i in all_wraps.find(class_="widget-row widget-row-days-date").find_all(class_="day")]
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
        response2.append("<b><u>📅 " + (all_dates[i]) + " | " + all_days[i] + "</u></b>" + "\n")
        response2[-1] += kb.slash
        response2[-1] += (
                kb.pogoda_stikers[kb.pogoda_picture_num.index(all_icon_phrases[i])] + " <b>" + kb.pogoda_phrase[
            kb.pogoda_picture_num.index(all_icon_phrases[i])] + "</b>" + " \n")
        response2[-1] += kb.slash
        response2[-1] += (
                "🌡️ <b>Ощущается как</b> " + t_feel_air[i][1] + " ℃  <b>-</b>  " + t_feel_air[i][0] + " ℃ \n ")
        response2[-1] += ("🌡️ <b>В среднем</b> " + t_avg_air[i] + " ℃ \n")
        response2[-1] += kb.slash
        response2[-1] += ("🌬 <b>Направление ветра</b> " + kb.arrows_directions[
            kb.arrows_directions_alp.index(wind_direction[i][1])] + " " + wind_direction[i][1] + " \n")
        response2[-1] += ("🌬 <b>Средняя скорость ветра</b> " + wind_avg_speed[i] + "м/c \n")
        response2[-1] += kb.slash
        response2[-1] += ("💧 <b>Относительная влажность</b> " + humidity[i] + " % \n")
        response2[-1] += kb.slash
        response2[-1] += ("🎚️ <b>Давление</b> " + pressure[i][0] + " мм. рт. ст. \n ")
        response2[-1] += kb.slash
        response2[-1] += ("☔ <b>Осадки</b> " + precipitation[i] + " мм")
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
    pic_tag = "#" + main_wrap.next["class"][1].replace('-', '_')

    main_states = [i.next.text for i in
                   main_wrap.find(class_="info-wrap").find_all(class_="item-value")]
    for i in range(len(main_states)):
        tmp = ''
        for j in range(len(main_states[i])):
            if (str(main_states[i][j]).isdigit() or main_states[i][j] in "+-"):
                tmp += main_states[i][j]
        main_states[i] = tmp

    if int(sunrise.split(":")[0]) > int(sunset.split(":")[0]):
        sunrise, sunset = sunset, sunrise

    response2.append(f"📅 <b><u>{data.strip()} |  {day.strip()} | {time.strip()} </u></b>{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += kb.pogoda_stikers[kb.pogoda_picture_num.index(pic_tag)] + " <b>" + str(
        desc.strip()) + "</b>" + kb.nl
    response2[-1] += kb.slash
    response2[-1] += (f"🌡️ <b>{temp} ℃</b>, ощущается как {temp_feel} ℃{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🌪️ <b>Ветер</b> {main_states[0]} м/с{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🎚️ <b>Давление</b> {main_states[1]} мм рт.ст.{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"💧 <b>Относительная влажность</b> {main_states[2]} %{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🧲 <b>Г/м активность</b> {main_states[3]} балла из 9{kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🌊 <b>Вода</b> {main_states[4]} °C {kb.nl}")
    response2[-1] += kb.slash
    response2[-1] += (f"🌇 <b>Восход</b> {sunrise}   ⤼   🌄 <b>Закат</b> {sunset}{kb.nl} ")

    return response2[0]


def get_day(city, day):
    try:
        url = "https://www.gismeteo.ru" + json_load[city] + str(day)
    except:
        url = ''
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    response2 = []
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
    all_wraps = soup.find("div", class_="widget-body widget-columns-8").find(class_="widget-items")
    all_times = [i.text[:-2] + " : " + i.text[-2:] for i in
                 all_wraps.find(class_="widget-row widget-row-time").find_all(class_="row-item")]

    all_icon_phrases = [i.find("use").get("href") for i in
                        all_wraps.find(class_="widget-row widget-row-icon").find_all(class_="row-item")]

    for i in all_wraps.find_all("div", class_="widget-row-chart widget-row-chart-temperature row-with-caption"):

        if i.get("data-row") == "temperature-air":
            for el in i.find_all(class_="value"):
                try:
                    t_air.append(el.find(class_="unit unit_temperature_c").text)
                except:
                    t_air.append("-")


        elif i.get("data-row") == "temperature-heat-index":
            for el in i.find_all(class_="value"):
                try:
                    t_feel_air.append(el.find(class_="unit unit_temperature_c").text)
                except:
                    t_feel_air.append("-")

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
            class_="value"):
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
    for i in range(8):
        response2.append("<b><u>" + (all_times[i]) + "</u></b>" + "\n")
        response2[-1] += kb.slash
        response2[-1] += (
                kb.pogoda_stikers[kb.pogoda_picture_num.index(all_icon_phrases[i])] + " <b>" + kb.pogoda_phrase[
            kb.pogoda_picture_num.index(all_icon_phrases[i])] + "</b>" + " \n")
        response2[-1] += kb.slash
        response2[-1] += ("🌡️ <b>Температура</b> " + str(t_air[i]) + " ℃  <b>-</b>  " + str(t_air[i]) + " ℃ \n ")
        response2[-1] += (
                "🌡️ <b>Ощущается как</b> " + str(t_feel_air[i]) + " ℃  <b>-</b>  " + str(t_feel_air[i]) + " ℃\n")
        response2[-1] += kb.slash
        response2[-1] += ("🌬 <b>Направление ветра</b> " + kb.arrows_directions[
            kb.arrows_directions_alp.index(wind_direction[i][1])] + " " + wind_direction[i][1] + " \n")
        response2[-1] += ("🌬 <b>Средняя скорость ветра</b> " + wind_avg_speed[i] + "м/c\n")
        response2[-1] += kb.slash
        response2[-1] += ("💧 <b>Относительная влажность</b> " + humidity[i] + " %\n")
        response2[-1] += kb.slash
        response2[-1] += ("🎚️ <b>Давление</b> " + pressure[i][0] + " мм. рт. ст.\n ")
        response2[-1] += kb.slash
        response2[-1] += ("☔ <b>Осадки</b> " + precipitation[i] + " мм")
    return response2


def get_3days(city):
    try:
        url = "https://www.gismeteo.ru" + json_load[city] + "3-days"
    except:
        url = ''
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    response2 = []
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
    all_wraps = soup.find("div", class_="widget widget-weather-parameters widget-threedays").find(class_="widget-items")
    all_days = [i.text for i in all_wraps.find(class_="widget-date-wrap").find_all(class_=re.compile("item"))[:3]]
    all_times = [i.text for i in
                 all_wraps.find(class_="widget-row widget-row-time").find_all(class_=re.compile("item"))[:12]]
    all_icon_phrases_with_desc = [[i.find("use")["href"], i.find(class_="weather-icon tooltip").get("data-text")] for i
                                  in
                                  all_wraps.find(class_="widget-row widget-row-icon").find_all(class_="row-item")[:12]]
    for i in all_wraps.find_all("div", class_="widget-row-chart widget-row-chart-temperature row-with-caption")[:12]:

        if i.get("data-row") == "temperature-air":
            for el in i.find_all(class_="value")[:12]:
                try:
                    t_air.append(el.find(class_="unit unit_temperature_c").text)
                except:
                    t_air.append("-")


        elif i.get("data-row") == "temperature-heat-index":
            for el in i.find_all(class_="value")[:12]:
                try:
                    t_feel_air.append(el.find(class_="unit unit_temperature_c").text)
                except:
                    t_feel_air.append("-")

    for el in all_wraps.find("div", {"data-row": "wind-speed"}).find_all(class_="row-item")[:12]:
        try:
            wind_avg_speed.append(el.find(class_="wind-unit unit unit_wind_m_s").text)
        except:
            wind_avg_speed.append("-")

    for el in all_wraps.find("div", {"data-row": "wind-gust"}).find_all(class_="row-item")[:12]:
        try:
            wind_gust.append(el.find(class_="wind-unit unit unit_wind_m_s").text)
        except:
            wind_gust.append("-")

    for el in all_wraps.find(class_="widget-row widget-row-precipitation-bars row-with-caption").find_all(
            class_="row-item")[:12]:
        try:
            precipitation.append(el.find(class_='item-unit').text)
        except:
            precipitation.append("-")

    for el in all_wraps.find(class_="widget-row-chart widget-row-chart-pressure row-with-caption").find_all(
            class_="value")[:12]:
        try:
            pressure.append([el.find(class_="mint").find(class_="unit unit_pressure_mm_hg_atm").text])
        except:
            pressure.append(["-"])
        try:
            pressure[-1].append(el.find(class_="maxt").find(class_="unit unit_pressure_mm_hg_atm").text)
        except:
            pressure[-1].append("-")

    for el in all_wraps.find(class_="widget-row widget-row-wind-direction row-with-caption").find_all(
            class_="row-item")[:12]:
        try:
            wind_direction.append([str(el.next.get("class")[-1][-1]), str(el.find(class_="direction").text)])
        except:
            wind_direction.append(["-", "-"])

    for el in all_wraps.find(class_="widget-row widget-row-humidity row-with-caption").find_all(
            class_=re.compile("row-item"))[:12]:
        try:
            humidity.append(el.text)
        except:
            humidity.append("-")

    for i in range(12):
        response2.append("<b><u>" + all_days[i // 4] + " | " + (all_times[i]) + "</u></b>" + "\n")
        response2[-1] += kb.slash
        response2[-1] += (
                kb.pogoda_stikers[kb.pogoda_picture_num.index(all_icon_phrases_with_desc[i][0])] + " <b>" +
                kb.pogoda_phrase[
                    kb.pogoda_picture_num.index(all_icon_phrases_with_desc[i][0])] + "</b>" + " \n")
        response2[-1] += kb.slash
        response2[-1] += f"🌡️ <b>Температура</b> {t_air[i]} ℃\n"
        if str(t_air[i]) != str(t_feel_air):
            response2[-1] += f"🌡️ <b>Ощущается как</b> {t_feel_air[i]} ℃\n"
        response2[-1] += kb.slash
        response2[
            -1] += f"🌬 <b>Направление ветра</b> {kb.arrows_directions[kb.arrows_directions_alp.index(wind_direction[i][1])]} {wind_direction[i][1]}\n"
        response2[-1] += f"🌬 <b>Средняя скорость ветра</b> {wind_avg_speed[i]} м/c\n"
        response2[-1] += kb.slash
        response2[-1] += f"💧 <b>Относительная влажность</b> {humidity[i]} %\n"
        response2[-1] += kb.slash
        response2[-1] += f"🎚️ <b>Давление</b> {pressure[i][0]} мм. рт. ст.\n"
        response2[-1] += kb.slash
        response2[-1] += f"☔ <b>Осадки</b> {precipitation[i]} мм"
    return response2


def get_one_from_ten(city, day_to_find=1):
    day_to_find -= 1
    try:
        url = "https://www.gismeteo.ru" + json_load[city] + "3-days"
    except:
        url = ''
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    response2 = []
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
    all_wraps = soup.find("div", class_="widget widget-weather-parameters widget-threedays").find(class_="widget-items")
    all_days = [i.text for i in all_wraps.find(class_="widget-date-wrap").find_all(class_=re.compile("item"))]
    all_times = [i.text for i in
                 all_wraps.find(class_="widget-row widget-row-time").find_all(class_=re.compile("item"))]
    all_icon_phrases_with_desc = [[i.find("use")["href"], i.find(class_="weather-icon tooltip").get("data-text")] for i
                                  in
                                  all_wraps.find(class_="widget-row widget-row-icon").find_all(class_="row-item")]
    for i in all_wraps.find_all("div", class_="widget-row-chart widget-row-chart-temperature row-with-caption"):

        if i.get("data-row") == "temperature-air":
            for el in i.find_all(class_="value"):
                try:
                    t_air.append(el.find(class_="unit unit_temperature_c").text)
                except:
                    t_air.append("-")


        elif i.get("data-row") == "temperature-heat-index":
            for el in i.find_all(class_="value"):
                try:
                    t_feel_air.append(el.find(class_="unit unit_temperature_c").text)
                except:
                    t_feel_air.append("-")

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
            class_="value"):
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
    print(all_days)
    print(all_times)
    for i in range(day_to_find, day_to_find + 4):
        response2.append("<b><u>" + all_days[i // 4] + " | " + (all_times[i]) + "</u></b>" + "\n")
        response2[-1] += kb.slash
        response2[-1] += (
                kb.pogoda_stikers[kb.pogoda_picture_num.index(all_icon_phrases_with_desc[i][0])] + " <b>" +
                kb.pogoda_phrase[
                    kb.pogoda_picture_num.index(all_icon_phrases_with_desc[i][0])] + "</b>" + " \n")
        response2[-1] += kb.slash
        response2[-1] += f"🌡️ <b>Температура</b> {t_air[i]} ℃\n"
        if str(t_air[day_to_find - 1]) != str(t_feel_air[i]):
            response2[-1] += f"🌡️ <b>Ощущается как</b> {t_feel_air[i]} ℃\n"
        response2[-1] += kb.slash
        response2[
            -1] += f"🌬 <b>Направление ветра</b> {kb.arrows_directions[kb.arrows_directions_alp.index(wind_direction[i][1])]} {wind_direction[i][1]}\n"
        response2[-1] += f"🌬 <b>Средняя скорость ветра</b> {wind_avg_speed[i]} м/c\n"
        response2[-1] += kb.slash
        response2[-1] += f"💧 <b>Относительная влажность</b> {humidity[i]} %\n"
        response2[-1] += kb.slash
        response2[-1] += f"🎚️ <b>Давление</b> {pressure[i][0]} мм. рт. ст.\n"
        response2[-1] += kb.slash
        response2[-1] += f"☔ <b>Осадки</b> {precipitation[i]} мм"
    return response2
