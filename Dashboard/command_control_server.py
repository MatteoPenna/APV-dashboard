import csv
from io import StringIO
import paho.mqtt.client as mqtt
import serial

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe('command/#')

def on_message(client, userdata, msg):
    if mqtt.topic_matches_sub('command/#', msg.topic):
        message_io = StringIO()
        csv.writer(message_io).writerow([msg.topic.split('/', 1)[1], msg.payload.decode('ascii')])
        ser.write(message_io.getvalue().encode('ascii'))

ser = serial.Serial('/dev/tty/AMA0', baudrate=115200)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost")

client.loop_start()

while True:
    for entry in csv.reader(StringIO(ser.readline().decode('ascii').strip())):
        client.publish('telemetry/' + entry[0], entry[1], retain=True)
