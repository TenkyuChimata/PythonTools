# -*- coding: utf-8 -*-
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from datetime import datetime, timedelta

client = Client(base_url = "https://data.raspberryshake.org")

def day_of_year(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month[2] = 29
    day_of_year = 0
    for m in range(1, month):
        day_of_year += days_in_month[m]
    day_of_year += day - 1
    return day_of_year

def save_data_for_date(date_string):
    date = UTCDateTime(date_string)
    seis_data = client.get_waveforms("AM", "RED68", "00", "EHZ", date, date + 86400)
    file_name = f"AM.RED68.00.EHZ.D.2023.{day_of_year(date_string):03d}"
    seis_data.write(file_name, format = "MSEED")
    print(f"Saved data for {date_string} to {file_name}")

start_date = "2023-01-01"
end_date = "2023-01-31"

current_date = start_date
while current_date <= end_date:
    save_data_for_date(current_date)
    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days = 1)).strftime("%Y-%m-%d")
