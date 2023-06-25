import json

import requests
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


def get_2week():
    url = "https://www.gismeteo.ru/weather-moscow-4368/2-weeks/"
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    soup = BeautifulSoup(response.text, "lxml")
    all_wraps = soup.find("div", class_="widget-body widget-columns-14").find(class_="widget-items")
    all_dates = [i.text for i in all_wraps.find(class_="widget-row widget-row-days-date").find_all(class_="date")]
    cur_month = ''
    for i in range(len(all_dates)):
        if len(all_dates[i].split()) > 1:
            cur_month = all_dates[i].split()[-1]
        else:
            all_dates[i] += ' ' + cur_month

    print(all_dates)
    all_icon_phrases = [i.find("use").get("href") for i in
                        all_wraps.find(class_="widget-row widget-row-icon").find_all(class_="row-item")]
    print(all_icon_phrases)
    t_air = []
    t_feel_air = []
    t_avg_air = []
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

    print(t_air)
    print(t_feel_air)
    print(t_avg_air)

    """
    for wrap in all_wraps:
        print(wrap.find(class_="widget-row widget-row-days-date") ,wrap,end=" ")
        if wrap.find(class_="widget-row widget-row-days-date") is not None:
            dates = []
            for el in wrap.find(class_="widget-row widget-row-days-date"):
                dates.append(el.find(class_="date"))
                print("hi")
            print(dates)
    """
