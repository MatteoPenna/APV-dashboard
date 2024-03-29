#So the general plan os to use the meta refresh in HTML set to 0
#in order to have the webpage constantly updating with new sensor
#information which is being placed into the HTML file. 

#To update the HTML file, I will use something called the SimpleTemplate
#Engine which exists in Flask. This will allow me use Python to 
#update the HTML file. 

#Therefore, I can subscribe to the MQTT topics for the sensor data
#and then store them in the program. Using the SimpleTemplate Engine
#I can then use Python to script those new values into the table.

#I can have two separate URLs, one to access sensor data and the 
#other to change following distance and click the kill switch.


from bottle import Bottle, route, run, static_file, debug, template, get
import paho.mqtt.client as mqtt
import time
import json

#declaring a global array for all of the data
data = [0] * 6

#creating a on_connect function which is called when the broker
#sees the connection request
def on_connect(client, userdata, flags, rc):
 #note:rc = connection result, 0 is successful

    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")

#rotations per min of the motor callback function
def rpm_callback(client, userdata, message):
    data[0] = int(message.payload)
    print('RPM : ' + str(data[0]))

#distance outputted by ultrasonic callback function
def distance_callback(client, userdata, message):  
    data[1] = int(message.payload)
    print('Distance : ' + str(data[1]))

#IMU callback 
def imu_callback(client, userdata, message):
    data[2] = int(message.payload)
    print('IMU :' + str(data[2]))

#battery temperature
def batteryTemp_callback(client, userdata, message):
    data[3] = int(message.payload)
    print('Battery Temp :' + str(data[3]))

#current outputted to the motor
def angularVelocity_callback(client, userdata, message):
    data[4] = int(message.payload)
    print('Motor Current :' + str(data[4]))

#voltage at the output of the battery
def batteryVoltage_callback(client, userdata, message):
    data[5] = int(message.payload)
    print('Battery Voltage :' + str(data[5]))

#connecting to MCU MQTT endpoint
broker_address = 'localhost'
port = 1883
print('creating new instance')
client = mqtt.Client()
print('connecting to broker')
client.on_connect = on_connect
client.connect(broker_address, port)
client.loop_start()

#waiting fro connection
time.sleep(0.1)

#setting message callback functions for telemetry
client.message_callback_add('telemetry/rpm',rpm_callback)
client.message_callback_add('telemetry/ultra_dist',distance_callback)
client.message_callback_add('telemetry/imu',imu_callback)
client.message_callback_add('telemetry/batt_temp',batteryTemp_callback)
client.message_callback_add('telemetry/angular_velocity',angularVelocity_callback)
client.message_callback_add('telemetry/batt_voltage',batteryVoltage_callback)

#function for subscribing to the main MQTT telemetry topic
client.subscribe('telemetry/#')

#function which will grab the from the MQTT control server
def grab_data(data):

    #setting each variable 
    R_wheel = 0.0325 #in m
    rpm = data[0]
    ultraDist = data[1]
    acceleration = data[2]
    batteryTemp = data[3]
    angularVelocity = data[4]
    batteryVoltage = data[5]
    speed = R_wheel*rpm/60 #calculating linear speed from RPM
 
    #setting up a dictionary using keyword arguments to pass the updated
    #values into the HTML template
    values = {
        'rpm' : str(rpm), 
        'ultraDist' : str(ultraDist), 
        'acceleration' : str(acceleration),
        'batteryTemp' : str(batteryTemp), 
        'angularVelocity' : str(angularVelocity), 
        'batteryVoltage' : str(batteryVoltage),
        'speed' : str(speed)
        }

    #returning each of the variables out of the function
    return (values)


#while true is needed to keep the 
while True:
        #exit handling
    try:
        #Bottle Code
        debug(True)
        @route('/js/jquery.min.js')
        def send_jquery():
            return static_file('/jquery.min.js', root = './js')

        @get('/get_data')
        def return_data():
            values_dict = grab_data(data)#grabs values from the data grab function
            return(json.dumps(values_dict))

        @get('/sensordash') #binds a piece of code to a url path
        def server_static():
            return template('./dashboard/table.tpl')

        run(host='localhost', port=8080, debug = True) #starts a built-in dev server

    
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()
        break



