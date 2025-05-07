# -*- coding: utf-8 -*-
import time
import tkinter
import tkinter.messagebox
import threading
from datetime import datetime, timedelta

def close():
    if tkinter.messagebox.askokcancel("退出", "确定要关闭吗?"):
        os._exit(0)

def gui():
    global nowtime_text
    tk = tkinter.Tk()
    tk.geometry("300x40")
    tk.title("Time")
    tk.configure(bg = "#232427")
    nowtime_text = tkinter.Label(tk, text = "2080-01-01 00:00:00", font = ("SDK_JP_Web", 19), fg = "white", bg = "#232427")
    nowtime_text.pack()
    tk.protocol("WM_DELETE_WINDOW", close)
    tk.mainloop()

def main():
    while True:
        nowtime_text.config(text = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)

thread1 = threading.Thread(target = gui)
thread2 = threading.Thread(target = main)
thread1.start()
time.sleep(1)
thread2.start()
