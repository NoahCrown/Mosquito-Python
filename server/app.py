from flask import Flask, jsonify
import pandas as pd
import joblib
import serial
import time
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)  # This allows all origins by default


regression_model = joblib.load('./model/larvae_model.pkl')



@app.route('/api/detection', methods=['GET'])
@cross_origin(origins=["http://localhost:3000"])

def detection():
    SERIAL_PORT = 'COM16'
    BAUD_RATE = 9600

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    if not ser.isOpen():
        ser.open()
    print('com11 open', ser.isOpen())

   
    x_vals = []
    ph_sensorval = []
    turbidity_sensorval = []
    dissolve_oxygen_sensorval = []
    temp_sensorval = []



    while (len(x_vals) < 3 ):
        line = ser.readline().decode('utf-8').strip()
    
        # Check if the line contains the initial message 'Ready'
        if line == 'Ready':
            return
        
        sensorValues = line.split(', ')
        time.sleep(3)
        # print(f"this si th sensor values {sensorValues}")
        x_vals.append(float(sensorValues[0]))
        ph_sensorval.append(float(sensorValues[1]))
        turbidity_sensorval.append(float(sensorValues[2]))
        dissolve_oxygen_sensorval.append(float(sensorValues[3]))
        temp_sensorval.append(float(sensorValues[4]))
        print(f'Time:{sensorValues[0]}, PH: {sensorValues[1]}, Turbidity: {sensorValues[2]}, Dissolve Oxygen: {sensorValues[3]}, Temp: {sensorValues[4]}')

    ph_avg = round(sum(ph_sensorval) / len(ph_sensorval), 2)
    turbidity_avg = round(sum(turbidity_sensorval) / len(turbidity_sensorval), 2)
    dissolve_oxygen_avg = round(sum(dissolve_oxygen_sensorval) / len(dissolve_oxygen_sensorval), 2)
    temp_avg = round(sum(temp_sensorval) / len(temp_sensorval), 2)

    print(ph_avg)
    print(turbidity_avg)
    print(dissolve_oxygen_avg)
    print(temp_avg)
    data = pd.DataFrame({
        'PH': [ph_avg],
        'Turbidity': [turbidity_avg],
        'Dissolve Oxygen': [dissolve_oxygen_avg],
        'Temp': [temp_avg]
    })

    predictions = regression_model.predict(data)
    print(predictions)
    predictions = [int(p) for p in predictions] 


    print(predictions)

    return {"predictions": predictions[0], "ph":ph_avg, "turbidity": turbidity_avg, "dissolve_oxygen": dissolve_oxygen_avg, "temp": temp_avg}, 200

if __name__ == '__main__':
    app.run(debug=True)