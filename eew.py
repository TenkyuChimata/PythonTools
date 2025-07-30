# -*- coding: utf-8 -*-
import math
import requests

current_lat = 30.68
current_long = 104.05
url = "https://api.wolfx.jp/cenc_eqlist.json"

def distance(lat1, lon1, lat2, lon2):
    radius = 6378.137
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d

def calculate_shindo(pga):
    calcshindo = round(round(2 * math.log10(pga) + 0.94, 3), 2)
    if calcshindo < 0.5:
        shindo = "0"
    elif calcshindo >= 0.5 and calcshindo < 1.5:
        shindo = "1"
    elif calcshindo >= 1.5 and calcshindo < 2.5:
        shindo = "2"
    elif calcshindo >= 2.5 and calcshindo < 3.5:
        shindo = "3"
    elif calcshindo >= 3.5 and calcshindo < 4.5:
        shindo = "4"
    elif calcshindo >= 4.5 and calcshindo < 5.0:
        shindo = "5弱"
    elif calcshindo >= 5.0 and calcshindo < 5.5:
        shindo = "5強"
    elif calcshindo >= 5.5 and calcshindo < 6.0:
        shindo = "6弱"
    elif calcshindo >= 6.0 and calcshindo < 6.5:
        shindo = "6強"
    elif calcshindo >= 6.5:
        shindo = "7"
    return shindo

if __name__ == '__main__':
    try:
        print("正在请求台网信息，请稍后...")
        print()
        cenc = requests.get(url, timeout = 5).json()
        print("获取成功，请输入地震序号和加速度：")
        print()
        for i in range(1, 11):
            if cenc[f"No{i}"]["type"] == "reviewed":
                auto_type = "正式"
            else:
                auto_type = "自动"
            eqdistance = distance(float(cenc[f"No{i}"]["latitude"]), float(cenc[f"No{i}"]["longitude"]), current_lat, current_long)
            print(f"[{i}] [{auto_type}] {cenc['No' + str(i)]['time']} {cenc['No' + str(i)]['location']} Ms{cenc['No' + str(i)]['magnitude']} 深度{cenc['No' + str(i)]['depth']}km 距离{eqdistance:.0f}km")
        order = input()
        pga = float(input())
        eqdate = cenc[f"No{order}"]["time"]
        eqdate_str = eqdate[:4] + "/" + eqdate[5:7] + "/" + eqdate[8:10] + eqdate[10:16]    
        print()
        print(f"{eqdate_str} {cenc[f'No{order}']['location']}Ms{cenc[f'No{order}']['magnitude']}地震观测 - 震度{calculate_shindo(pga)}【地震预警】")
        print()
        eqdate = cenc[f"No{order}"]["time"]
        eqdate_str = eqdate[:4] + "年" + eqdate[5:7] + "月" + eqdate[8:10] + "日" + eqdate[11:]
        eqdistance = distance(float(cenc[f"No{order}"]["latitude"]), float(cenc[f"No{order}"]["longitude"]), current_lat, current_long)
        print(f"{cenc[f'No{order}']['location']}Ms{cenc[f'No{order}']['magnitude']} 震源深度{cenc[f'No{order}']['depth']}km")
        print(f"发生于北京时间{eqdate_str}")
        print(f"本地观测点数据：最大加速度{pga}gal")
        # print(f"本地观测点数据：四川成都|距震中约{eqdistance:.0f}km|最大加速度{pga}gal")
    except Exception as e:
        print(e)
    # time.sleep(999)
