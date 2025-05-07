import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def read_serial_data(ser):
    try:
        line = ser.readline()
        line = line.decode('utf-8', errors='ignore').strip()
        values = list(map(int, line.split('\t')))
        if len(values) == 3:
            return values
    except Exception as e:
        print(f"Error reading serial data: {e}")
    return None

def update_plot(frame, ser, x_data, y_data, z_data, lines):
    while ser.in_waiting:
        data = read_serial_data(ser)
        if data is not None:
            x, y, z = data
            
            x_data.append(x - 10000)
            y_data.append(y)  # 增加 Y 轴的偏移量
            z_data.append(z)  # 增加 Z 轴的偏移量
            
            if len(x_data) > 500:
                x_data.pop(0)
                y_data.pop(0)
                z_data.pop(0)
    
    if len(x_data) > 0:
        lines[0].set_data(range(len(x_data)), x_data)
        lines[1].set_data(range(len(y_data)), y_data)
        lines[2].set_data(range(len(z_data)), z_data)
    
    return lines

def main():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    
    fig, ax = plt.subplots()
    ax.set_ylim(-32768, 32768)
    ax.set_xlim(0, 500)
    ax.set_title("Real-time Serial Data Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Sensor Readings")
    
    x_data, y_data, z_data = [], [], []
    line_x, = ax.plot([], [], label='X-Axis')
    line_y, = ax.plot([], [], label='Y-Axis')
    line_z, = ax.plot([], [], label='Z-Axis')
    
    ax.legend()
    
    ani = animation.FuncAnimation(fig, update_plot, fargs=(ser, x_data, y_data, z_data, [line_x, line_y, line_z]), interval=10, cache_frame_data=False)
    plt.show()
    
    ser.close()

if __name__ == "__main__":
    main()
