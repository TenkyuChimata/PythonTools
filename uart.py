import serial
import threading

# 配置串口参数
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# 确保串口打开
if ser.isOpen():
    print("串口已打开")

# 接收数据的函数
def read_from_port():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()  # 读取一行数据
            if data:
                print(f"\n接收到的数据: {data}")

# 创建一个线程用于接收数据
read_thread = threading.Thread(target=read_from_port, daemon=True)
read_thread.start()

try:
    while True:
        # 手动输入要发送的内容
        user_input = input()
        if user_input.lower() == 'exit':
            break
        ser.write(user_input.encode('utf-8'))  # 将输入转换为字节并发送
        print(f"已发送: {user_input}")
except KeyboardInterrupt:
    print("\n手动终止发送")

# 关闭串口
ser.close()
print("串口已关闭")
