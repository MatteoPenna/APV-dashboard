from bottle import Bottle, route, run, static_file, debug, template, request, get
import paho.mqtt.client as mqtt
import time
import json
#declaring a global array for all of the data
data = [0] * 6

#-----------------------#
#BEGINNING OF MQTT CODE
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
    #print('RPM : ' + str(data[0]))

#distance outputted by ultrasonic callback function
def distance_callback(client, userdata, message):  
    data[1] = int(message.payload)
    #print('Distance : ' + str(data[1]))

#IMU callback 
def imu_callback(client, userdata, message):
    data[2] = int(message.payload)
    #print('IMU :' + str(data[2]))

#battery temperature
def batteryTemp_callback(client, userdata, message):
    data[3] = int(message.payload)
    #print('Battery Temp :' + str(data[3]))

#current outputted to the motor
def angularVelocity_callback(client, userdata, message):
    data[4] = int(message.payload)
    #print('Motor Current :' + str(data[4]))

#voltage at the output of the battery
def batteryVoltage_callback(client, userdata, message):
    data[5] = int(message.payload)
    #print('Battery Voltage :' + str(data[5]))

#create function for callback
def on_publish(client,userdata,result):             
    print("data published \n")

#connecting to MCU MQTT endpoint
broker_address = 'localhost'
print('creating new instance')
client = mqtt.Client()
print('connecting to broker')
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address) #establishing connection
client.loop_start()

#waiting for connection
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

#END OF MQTT CODE
#------------------#

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
        #Bottle code
        debug(True)
        @route('/dashboard') #binds a piece of code to a url path
        def send_site():
            #function will serve up the control dashboard html page
            return template('./dashboard-final.tpl')

        @route('/js/jquery.min.js')
        def send_jquery():
            #function serving jquery code
            return static_file('/jquery.min.js', root = './js')

        @route('/killed', method = 'POST')
        def send_killed():
            #publishing kill command
            client.publish("command/power", 0, retain = True) #publish to speed
            return '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <!--<meta http-equiv="refresh" content="2; url=http://localhost:8080/controldash">-->
                    </head>
                    <body>
                    <div>
                    APV has been killed.
                    </div>
                    </body>
                    </html>
                    '''
        @route('/hyper_params/decision', method = 'POST')
        def send_decision_params():
            #pulling  values from POST
            decision_params = request.json
            client.publish("hyper_params/decision",
                json.dumps(decision_params), retain = True)
            print(decision_params)

        @route('/hyper_params/image_processing', method = 'POST')
        def send_image_processing_params():
            #pulling values from POST and publishing them
            client.publish("hyper_params/decision",
                json.dumps(request.json), retain = True)
            print(json.dumps(request.json))           

        @route('/hyper_params/image_capture', method = 'POST')   
        def send_image_capture_params():
            image_capture_params = request.json
            client.publish("hyper_params/decision",
                json.dumps(image_capture_params), retain = True)
            print(image_capture_params) 

        @route('/speed_and_angle', method = 'POST')
        def process_data():
            #extract data from POST
            angle = request.forms.get('angle') #in degrees
            speed = request.forms.get('speed') #in km/h
            print(speed,angle)
            #process html form and publish data to mqtt
            client.publish("command/wheel_speed", speed, retain = True) #publish to speed
            client.publish("command/steering", angle, retain = True) #publish to steering

        @get('/get_data')
        def return_data():
            values_dict = grab_data(data)#grabs values from the data grab function
            return(json.dumps(values_dict))

        run(host='localhost', port=8080, debug = True) #starts a built-in dev server

    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()
        break
