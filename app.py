from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import json
import serial
import threading
import time
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')



current_number = 1
increment = True

def generate_and_send_number():
    global current_number, increment

    while True:
        # Send the current number to the client
        socketio.emit('receive_number', {'random_number': current_number})

        # Update the number for the next iteration
        if increment:
            current_number += 1
            if current_number >= 70:
                increment = False
        else:
            current_number -= 1
            if current_number <= 1:
                increment = True
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    # Start a background thread to generate and send numbers
    threading.Thread(target=generate_and_send_number).start()




@socketio.on('request_arduino')
def read_arduino_data():
    try:
        # Подключение к порту (например, COM3)
        with serial.Serial('COM7', 9600) as ser:  
            # Чтение данных из порта
            data = ser.readline().decode('utf-8', errors='ignore').strip()

            # Проверка JSON-формата
            if data.startswith('{') and data.endswith('}'):
                # Преобразование JSON-строки в Python-словарь
                jsonData = json.loads(data)
                # Извлечение данных из JSON
                sensorValue = jsonData.get("sensorSpeed") #ускорение
                sensorValue1 = jsonData.get("sensorHigh") #высота
                sensorValue2 = jsonData.get("sensorDavlen") #давление
                sensorValue3 = jsonData.get("sensorTemp") #температура
                sensorValue4 = jsonData.get("sensorHumidy") #Влажность
                sensorValue5 = jsonData.get("sensorSpeedy") #Скорость
                sensorValue6 = jsonData.get("sensorCO") #Кислород
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print (f"Acceleration: {sensorValue}, Altitude: {sensorValue1}, Pressure: {sensorValue2}, "
                f"Temperature: {sensorValue3}, Humidity: {sensorValue4}, Speed: {sensorValue5}, "
                f"Co2: {sensorValue6}, Current Time: {current_time}\n")
                
                # Проверка наличия данных
                if sensorValue is not None and sensorValue1 is not None:
                    # Отправка данных через socketio
                    socketio.emit('receive_arduino', {"sensorSpeed": sensorValue})
                    socketio.emit('receive_arduino1', {"sensorHigh": sensorValue1})
                    socketio.emit('receive_arduino2', {"sensorDavlen": sensorValue2})
                    socketio.emit('receive_arduino3', {"sensorTemp": sensorValue3})
                    socketio.emit('receive_arduino4', {"sensorHumidy": sensorValue4})
                    socketio.emit('receive_arduino5', {"sensorSpeedy": sensorValue5})
                    socketio.emit('receive_arduino6', {"sensorCO": sensorValue6})

                    return sensorValue, sensorValue1,sensorValue2, sensorValue3
    except (serial.SerialException, json.JSONDecodeError):
        pass


if __name__ == '__main__':
    app.run(debug=True)
