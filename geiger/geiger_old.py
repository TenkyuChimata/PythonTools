# -*- coding: utf-8 -*-
import time
import math
import requests
import colorama
import threading
#import traceback

url = "http://192.168.0.13/data.json"
url_qw = "https://devapi.qweather.com/v7/weather/now?key=&location="
colorama.init(autoreset = True)

def get_windspeed():
    global wind_speed
    wind_speed = 1
    while(1):
        try:
            data = requests.get(url_qw, timeout = 3)
            data_json = data.json()
            wind_speed = int(data_json["now"]["windSpeed"])
            if wind_speed <= 0:
                wind_speed = 1
            time.sleep(120)
        except:
            wind_speed = 1
            time.sleep(60)

def get_data():
    try:
        data = requests.get(url, timeout = 3)
        data_json = data.json()
        temperature = data_json["temperature"]
        humidity = data_json["humidity"]
        pressure = data_json["pressure"]
        pm25 = data_json["pm2.5"]
        pm10 = data_json["pm10"]
        create_at = data_json["create_at"]
        dew_point = data_json["dew_point"]
    except:
        temperature, humidity, pressure, pm25, pm10, dew_point = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        create_at = "2000-01-01 00:00:00"
    return(temperature, humidity, pressure, pm25, pm10, create_at, dew_point)

def main():
    while(1):
        try:
            weather_data = get_data()
            temperature = weather_data[0]
            humidity = weather_data[1]
            pressure = weather_data[2]
            pm25 = weather_data[3]
            pm10 = weather_data[4]
            dew_point = weather_data[6]
            apparent_temp = 1.07 * temperature + 0.2 * ((humidity / 100) * 6.105 * math.exp((17.27 * temperature) / (237.7 + temperature))) - 0.65 * wind_speed - 2.7
            discomfort_index = 0.81 * temperature + humidity * 0.01 * (0.99 * temperature -14.3) + 46.3
            print()
            print(weather_data[5], "实时室外环境数据(四川成都)")
            if temperature > 0 and temperature <= 15:
                print("温度" + colorama.Fore.CYAN + "%.1f℃" %temperature, end = " ")
            elif temperature > 15 and temperature <= 25:
                print("温度" + colorama.Fore.GREEN + "%.1f℃" %temperature, end = " ")
            elif temperature > 25 and temperature <= 35:
                print("温度" + colorama.Fore.YELLOW + "%.1f℃" %temperature, end = " ")
            elif temperature > 35:
                print("温度" + colorama.Fore.RED + "%.1f℃" %temperature, end = " ")
            else:
                print("温度" + colorama.Fore.BLUE + "%.1f℃" %temperature, end = " ")
            if humidity > 50:
                print("湿度" + colorama.Fore.CYAN + "%.f" %humidity + "%", end = " ")
            else:
                print("湿度" + colorama.Fore.YELLOW + "%.f" %humidity + "%", end = " ")
            if pressure > 1050:
                print("气压" + colorama.Fore.CYAN + "%.2fhPa" %pressure, end = " ")
            elif pressure < 950:
                print("气压" + colorama.Fore.YELLOW + "%.2fhPa" %pressure, end = " ")
            else:
                print("气压" + colorama.Fore.GREEN + "%.2fhPa" %pressure, end = " ")
            print("空气质量")
            if pm25 > 35 and pm25 <= 75:
                print("PM2.5 " + colorama.Fore.CYAN + "%.1fug/m³" %pm25 + colorama.Fore.RESET + "(良好)", end = " ")
            elif pm25 > 75 and pm25 <= 115:
                print("PM2.5 " + colorama.Fore.BLUE + "%.1fug/m³" %pm25 + colorama.Fore.RESET + "(轻度)", end = " ")
            elif pm25 > 115 and pm25 <= 150:
                print("PM2.5 " + colorama.Fore.YELLOW + "%.1fug/m³" %pm25 + colorama.Fore.RESET + "(中度)", end = " ")
            elif pm25 > 150 and pm25 <= 250:
                print("PM2.5 " + colorama.Fore.RED + "%.1fug/m³" %pm25 + colorama.Fore.RESET + "(重度)", end = " ")
            elif pm25 > 250:
                print("PM2.5 " + colorama.Fore.RED + "%.1fug/m³" %pm25 + colorama.Fore.RESET + "(严重)", end = " ")
            else:
                print("PM2.5 " + colorama.Fore.GREEN + "%.1fug/m³" %pm25 + colorama.Fore.RESET + "(优秀)", end = " ")
            if pm10 > 40 and pm10 <= 70:
                print("PM10 " + colorama.Fore.YELLOW + "%.1fug/m³" %pm10 + colorama.Fore.RESET + "(二级)")
            elif pm10 > 70:
                print("PM10 " + colorama.Fore.RED + "%.1fug/m³" %pm10 + colorama.Fore.RESET + "(严重)")
            else:
                print("PM10 " + colorama.Fore.GREEN + "%.1fug/m³" %pm10 + colorama.Fore.RESET + "(一级)")
            if dew_point > 15 and dew_point <= 20:
                print("露点温度" + colorama.Fore.YELLOW + "%.1f℃" %dew_point, end = " ")
            elif dew_point > 20:
                print("露点温度" + colorama.Fore.RED + "%.1f℃" %dew_point, end = " ")
            else:
                print("露点温度" + colorama.Fore.GREEN + "%.1f℃" %dew_point, end = " ")
            if apparent_temp > 0 and apparent_temp <= 15:
                print("体感温度" + colorama.Fore.CYAN + "%.1f℃" %apparent_temp, end = " ")
            elif apparent_temp > 15 and apparent_temp <= 25:
                print("体感温度" + colorama.Fore.GREEN + "%.1f℃" %apparent_temp, end = " ")
            elif apparent_temp > 25 and apparent_temp <= 35:
                print("体感温度" + colorama.Fore.YELLOW + "%.1f℃" %apparent_temp, end = " ")
            elif apparent_temp > 35:
                print("体感温度" + colorama.Fore.RED + "%.1f℃" %apparent_temp, end = " ")
            else:
                print("体感温度" + colorama.Fore.BLUE + "%.1f℃" %apparent_temp, end = " ")
            if discomfort_index >= 50 and discomfort_index < 55:
                print("不适指数" + colorama.Fore.BLUE + "%.f" %discomfort_index + colorama.Fore.RESET + "(寒冷)")
            elif discomfort_index >= 55 and discomfort_index < 60:
                print("不适指数" + colorama.Fore.CYAN + "%.f" %discomfort_index + colorama.Fore.RESET + "(较冷)")
            elif discomfort_index >= 60 and discomfort_index < 70:
                print("不适指数" + colorama.Fore.GREEN + "%.f" %discomfort_index + colorama.Fore.RESET + "(舒适)")
            elif discomfort_index >= 70 and discomfort_index < 75:
                print("不适指数" + colorama.Fore.YELLOW + "%.f" %discomfort_index + colorama.Fore.RESET + "(较热)")
            elif discomfort_index >= 75 and discomfort_index < 85:
                print("不适指数" + colorama.Fore.RED + "%.f" %discomfort_index + colorama.Fore.RESET + "(炎热)")
            elif discomfort_index >= 85:
                print("不适指数" + colorama.Fore.RED + "%.f" %discomfort_index + colorama.Fore.RESET + "(酷热)")
            else:
                print("不适指数" + colorama.Fore.RED + "%.f" %discomfort_index + colorama.Fore.RESET + "(极寒)")
            time.sleep(60)
        except:
            #traceback.print_exc()
            continue

thread1 = threading.Thread(target = get_windspeed)
thread2 = threading.Thread(target = main)
thread1.start()
time.sleep(1)
thread2.start()
