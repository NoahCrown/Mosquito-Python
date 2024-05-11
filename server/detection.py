import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import time

SERIAL_PORT = 'COM16'
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

x_vals = []
ph_sensorval = []
turbidity_sensorval = []
dissolve_oxygen_sensorval = []
temp_sensorval = []

def read_and_process_data():
    line = ser.readline().decode('utf-8').strip()
    
    # Check if the line contains the initial message 'Ready'
    if line == 'Ready':
        return
    
    sensorValues = line.split(', ')

    x_vals.append(float(sensorValues[0]))
    ph_sensorval.append(float(sensorValues[1]))
    turbidity_sensorval.append(float(sensorValues[2]))
    dissolve_oxygen_sensorval.append(float(sensorValues[3]))
    temp_sensorval.append(float(sensorValues[4]))
    
    print(f'Time:{sensorValues[0]}, PH: {sensorValues[1]}, Turbidity: {sensorValues[2]}, Dissolve Oxygen: {sensorValues[3]}, Temp: {sensorValues[4]}')
    time.sleep(3)
def update_plot(frame):
    read_and_process_data()
    plt.cla()
    plt.plot(x_vals, ph_sensorval, label='PH')
    plt.plot(x_vals, turbidity_sensorval, label='Turbidity')
    plt.plot(x_vals, dissolve_oxygen_sensorval, label='Dissolve Oxygen')
    plt.plot(x_vals, temp_sensorval, label='Temp')
    plt.xlabel('Time')
    plt.ylabel('Sensor Values')
    plt.legend()

def on_close(event):
    with open('arduino_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PH', 'Turbidity', 'Dissolve Oxygen', 'Temp'])
        for ph, turbi, do, temp in zip(ph_sensorval, turbidity_sensorval, dissolve_oxygen_sensorval, temp_sensorval):
            writer.writerow([ph, turbi, do, temp])

fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update_plot, interval=10)
plt.show()
