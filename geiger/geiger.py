# -*- coding: utf-8 -*-
import vlc
import time
import psutil
import requests
import colorama
import threading

url = "https://station.wolfx.jp/data.json"
colorama.init(autoreset = True)

def get_data():
    try:
        data_json = requests.get(url, timeout = 5).json()
        temperature = data_json["temperature"]
        humidity = data_json["humidity"]
        pressure = data_json["pressure"]
        pm25 = data_json["pm2.5"]
        pm10 = data_json["pm10"]
        usv = data_json["usv"]
        usv_avg = data_json["usv_avg"]
    except:
        temperature, humidity, pressure, pm25, pm10, usv, usv_avg = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    return(temperature, humidity, pressure, pm25, pm10, usv, usv_avg)

def alert():
    vlcplay = vlc.MediaPlayer("./assets/sounds/alert.wav")
    vlcplay.play()
    time.sleep(1)
    vlcplay.stop()

def main():
    while True:
        try:
            weather_data = get_data()
            temperature = weather_data[0]
            humidity = weather_data[1]
            pressure = weather_data[2]
            pm25 = weather_data[3]
            pm10 = weather_data[4]
            usv = weather_data[5]
            usv_avg = weather_data[6]
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage("/").percent
            if usv >= 0.4:
                thread1 = threading.Thread(target = alert)
                thread1.start()
            print()
            print()
            if temperature > 0 and temperature <= 15:
                print(f"温度{colorama.Fore.CYAN}{temperature:.1f}℃", end = " ")
            elif temperature > 15 and temperature <= 25:
                print(f"温度{colorama.Fore.GREEN}{temperature:.1f}℃", end = " ")
            elif temperature > 25 and temperature <= 35:
                print(f"温度{colorama.Fore.YELLOW}{temperature:.1f}℃", end = " ")
            elif temperature > 35:
                print(f"温度{colorama.Fore.RED}{temperature:.1f}℃", end = " ")
            else:
                print(f"温度{colorama.Fore.BLUE}{temperature:.1f}℃", end = " ")
            if humidity > 50:
                print(f"湿度{colorama.Fore.CYAN}{humidity:.0f}%", end = " ")
            else:
                print(f"湿度{colorama.Fore.YELLOW}{humidity:.0f}%", end = " ")
            if pressure > 1050:
                print(f"气压{colorama.Fore.CYAN}{pressure:.2f}hPa")
            elif pressure < 950:
                print(f"气压{colorama.Fore.YELLOW}{pressure:.2f}hPa")
            else:
                print(f"气压{colorama.Fore.GREEN}{pressure:.2f}hPa")
            if pm25 > 35 and pm25 <= 75:
                print(f"PM2.5 {colorama.Fore.CYAN}{pm25:.1f}ug/m³", end = " ")
            elif pm25 > 75 and pm25 <= 115:
                print(f"PM2.5 {colorama.Fore.BLUE}{pm25:.1f}ug/m³", end = " ")
            elif pm25 > 115 and pm25 <= 150:
                print(f"PM2.5 {colorama.Fore.YELLOW}{pm25:.1f}ug/m³", end = " ")
            elif pm25 > 150 and pm25 <= 250:
                print(f"PM2.5 {colorama.Fore.RED}{pm25:.1f}ug/m³", end = " ")
            elif pm25 > 250:
                print(f"PM2.5 {colorama.Fore.RED}{pm25:.1f}ug/m³", end = " ")
            else:
                print(f"PM2.5 {colorama.Fore.GREEN}{pm25:.1f}ug/m³", end = " ")
            if pm10 > 40 and pm10 <= 70:
                print(f"PM10 {colorama.Fore.YELLOW}{pm10:.1f}ug/m³")
            elif pm10 > 70:
                print(f"PM10 {colorama.Fore.RED}{pm10:.1f}ug/m³")
            else:
                print(f"PM10 {colorama.Fore.GREEN}{pm10:.1f}ug/m³")
            if usv >= 0.4:
                usv_color = colorama.Fore.RED
            else:
                usv_color = colorama.Fore.GREEN
            if usv >= 10.0 and usv < 100.0:
                print(f"电离辐射 {usv_color}{usv:.1f}uSv/h", end = "")
            elif usv >= 100.0 and usv < 1000.0:
                print(f"电离辐射 {usv_color}{usv:.0f}uSv/h", end = "")
            elif usv >= 1000.0:
                print(f"电离辐射 {usv_color}{usv / 1000:.2f}mSv/h", end = "")
            else:
                print(f"电离辐射 {usv_color}{usv:.2f}uSv/h", end = "")
            if usv_avg >= 0.4:
                usv_avg_color = colorama.Fore.RED
            else:
                usv_avg_color = colorama.Fore.GREEN
            if usv_avg >= 10.0 and usv_avg < 100.0:
                print(f"{usv_avg_color} ({usv_avg:.1f}uSv/h)")
            elif usv_avg >= 100.0 and usv_avg < 1000.0:
                print(f"{usv_avg_color} ({usv_avg:.0f}uSv/h)")
            elif usv_avg >= 1000.0:
                print(f"{usv_avg_color} ({usv_avg / 1000:.2f}mSv/h)")
            else:
                print(f"{usv_avg_color} ({usv_avg:.2f}uSv/h)")
            if cpu_percent > 50 and cpu_percent <= 80:
                print(f"CPU {colorama.Fore.YELLOW}{cpu_percent}%", end = " ")
            elif cpu_percent > 80:
                print(f"CPU {colorama.Fore.RED}{cpu_percent}%", end = " ")
            else:
                print(f"CPU {colorama.Fore.GREEN}{cpu_percent}%", end = " ")
            if ram_percent > 50 and ram_percent <= 80:
                print(f"RAM {colorama.Fore.YELLOW}{ram_percent}%", end = " ")
            elif ram_percent > 80:
                print(f"RAM {colorama.Fore.RED}{ram_percent}%", end = " ")
            else:
                print(f"RAM {colorama.Fore.GREEN}{ram_percent}%", end = " ")
            if disk_percent > 50 and disk_percent <= 80:
                print(f"HDD {colorama.Fore.YELLOW}{disk_percent}%")
            elif disk_percent > 80:
                print(f"HDD {colorama.Fore.RED}{disk_percent}%")
            else:
                print(f"HDD {colorama.Fore.GREEN}{disk_percent}%")
            print("\n")
            time.sleep(60)
        except Exception as e:
            #print(e)
            time.sleep(1)
            continue

main()
