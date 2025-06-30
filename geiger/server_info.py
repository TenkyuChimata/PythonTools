# -*- coding: utf-8 -*-
import time
import flask
import psutil
import datetime
import threading
import flask_cors

# 初始化数据存储
data = {
    "cpu_percent": 0.0,
    "ram_percent": 0.0,
    "disk_percent": 0.0,
    "update_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

app = flask.Flask("SERVERINFOAPI")
flask_cors.CORS(app)

def measure_system_usage():
    """
    定时测量系统资源使用情况，每 5 秒更新一次
    """
    global data
    while True:
        try:
            while True:
                cpu_percent = psutil.cpu_percent(interval=5)
                if cpu_percent < 99.9:
                    break
            ram_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage("/").percent
            # 更新数据
            data.update({
                "cpu_percent": cpu_percent,
                "ram_percent": ram_percent,
                "disk_percent": disk_percent,
                "update_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # 如果发生异常，等待 5 秒后重试

@app.route("/api/server_info", methods=["GET"])
def get_api():
    """
    提供服务器资源使用情况的 API
    """
    return flask.jsonify(data)

if __name__ == '__main__':
    # 启动后台线程以更新系统使用情况
    thread1 = threading.Thread(target=measure_system_usage)
    thread1.daemon = True  # 设置为守护线程
    thread1.start()
    app.run(host="0.0.0.0", port=4999)
