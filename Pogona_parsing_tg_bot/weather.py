import requests
from bs4 import BeautifulSoup

url = "https://www.gismeteo.ru/weather-moscow-4368/month"
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})
# all_possible_tiems = ["now", "tomorrow", "3-days", "10-days", "2-weeks", ""]
soup = BeautifulSoup(response.text, "lxml")
all_wraps = soup.find("div", class_="widget widget-month").find_all(class_="row-item")
cur_month = ''
file = open("weather_response", "w")
for wrap in all_wraps:
    mint = wrap.find(class_="mint").find(class_="unit unit_temperature_c").text
    maxt = wrap.find(class_="maxt").find(class_="unit unit_temperature_c").text
    date = wrap.find(class_="date").text
    if len(date.split()) > 1:
        cur_month = date.split()[-1]
    print(date if len(date.split()) > 1 else date + str(' ' + cur_month), end=' ')
    file.write(date + ": " if len(date.split()) > 1 else date + str(' ' + cur_month) + ': ')
    print("минимальная температура: ", mint, "      максимальная температура: ", maxt)
    file.write("минимальная температура: " + str(mint) + "      максимальная температура: " + maxt + '\n')
    # data = wrap.find(class_="date").text
    # time = wrap.find(class_="day").text
    # all_temps = wrap.find_all(class_="unit unit_temperature_c")
    # temp_mech = all_temps[0].text
    # temp_feel = all_temps[1].text
    # print(data, time,"  температура:",temp_mech, "по ощущению:" ,temp_feel)

file.close()
