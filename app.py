from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import json
import serial
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('request_number')
def generate_random_number():
   random_number = random.randint(1, 100)
   print(random_number)
   time.sleep(2)
   socketio.emit('receive_number', {'random_number': random_number})


@socketio.on('request_arduino')
def read_arduino_data():
    try:
        # Подключение к порту (например, COM3)
        with serial.Serial('COM3', 9600) as ser:  
            # Чтение данных из порта
            data = ser.readline().decode('utf-8').strip()

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
                #print(sensorValue, sensorValue1, sensorValue2, sep=' ')

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
