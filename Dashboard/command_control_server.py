import csv
from io import StringIO
import paho.mqtt.client as mqtt
import serial
import random
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    #client.subscribe('command/#')

def on_message(client, userdata, msg):
    '''
    if mqtt.topic_matches_sub('command/#', msg.topic):
        message_io = StringIO()
        csv.writer(message_io).writerow([msg.topic.split('/', 1)[1], msg.payload.decode('ascii')])
        ser.write(message_io.getvalue().encode('ascii'))
    '''

#ser = serial.Serial('COM8', baudrate=115200)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost")

client.loop_start()

start = time.time()

while True:
    time.sleep(1)
    random.seed(1)
    values = [0] * 6
    valueName = [
        'rpm',
        'ultra_dist',
        'imu',
        'batt_temp',
        'angular_velocity',
        'batt_voltage']

    
    while True:
        for i in range(0,6):
            values[i] = random.randint(0,10)

        time.sleep(0.1)

        for i in range(0,6):
            client.publish('telemetry/' + valueName[i], values[i], retain=True)

        print(values)

