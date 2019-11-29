from bottle import Bottle, route, run, static_file, debug, template, request, get
import paho.mqtt.client as mqtt
import time
import json
import sys

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
    sensor_data[0] = message.payload.decode('ascii')
    #print('RPM : ' + str(sensor_data[0]))

#distance outputted by ultrasonic callback function
def distance_callback(client, userdata, message):  
    sensor_data[1] = message.payload.decode('ascii').split(',')
    #print('Distance : ' + str(sensor_data[1]))

#IMU callback 
def imu_callback(client, userdata, message):
    sensor_data[2] = int(message.payload)
    #print('IMU :' + str(sensor_data[2]))

#battery temperature
def batteryTemp_callback(client, userdata, message):
    sensor_data[3] = message.payload.decode('ascii').split(',')
    #print('Battery Temp :' + str(sensor_data[3]))

#angular velocity of the APV
def angularVelocity_callback(client, userdata, message):
    sensor_data[4] = message.payload.decode('ascii')
    #print('Motor Current :' + str(sensor_data[4]))

#voltage at the output of the battery
def batteryVoltage_callback(client, userdata, message):
    sensor_data[5] = message.payload.decode('ascii')
    #print('Battery Voltage :' + str(sensor_data[5]))

#returns the outputted rpm value from the driving algorithm   
def outputted_values(client, userdata, message):
    #updating global dict 
    dump = json.loads(message.payload)
    current_vals[0] = dump['rpm']
    current_vals[1] = dump['current_distance']
    current_vals[2] = dump['current_angle']
    #print(current_vals)

#create function for callback
def on_publish(client,userdata,result):             
    print("data published \n")
    
def mqtt_connect():
    #connecting to MCU MQTT endpoint
    broker_address = 'localhost'
    print('creating new instance')
    client = mqtt.Client()
    print('connecting to broker')
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker_address) #establishing connection
    return client
    
def add_call_backs(client):
    #setting message callback functions for telemetry and program_outputs
    client.message_callback_add('telemetry/rpm',rpm_callback)
    client.message_callback_add('telemetry/ultra_dist',distance_callback)
    client.message_callback_add('telemetry/imu',imu_callback)
    client.message_callback_add('telemetry/batt_temp',batteryTemp_callback)
    client.message_callback_add('telemetry/angular_velocity',angularVelocity_callback)
    client.message_callback_add('telemetry/batt_voltage',batteryVoltage_callback)
    client.message_callback_add('program_outputs/current_values', outputted_values)

#END OF MQTT CODE
#------------------#

#function which will grab the from the MQTT control server
def grab_data(sensor_data):

    #setting each variable 
    R_wheel = 0.0325 #in m
    rpm = sensor_data[0]
    ultraDist = sensor_data[1]
    acceleration = sensor_data[2]
    batteryTemp = sensor_data[3]
    angularVelocity = sensor_data[4]
    batteryVoltage = sensor_data[5]
    speed = 10 #R_wheel*rpm/60 #calculating linear speed from RPM
 
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
    
def web_server():
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
        client.publish("command/power", 0) #publish to power
   
    @route('/hyper_params/decision', method = 'POST')
    def send_decision_params():
        #pulling  values from POST
        decision_params = request.json
        client.publish("hyper_params/decision",
            json.dumps(decision_params))
        print(decision_params)

    @route('/hyper_params/image_processing', method = 'POST')
    def send_image_processing_params():
        #pulling values from POST and publishing them
        client.publish("hyper_params/image_processing",
            json.dumps(request.json))
        print(json.dumps(request.json))           

    @route('/hyper_params/image_capture', method = 'POST')   
    def send_image_capture_params():
        image_capture_params = request.json
        client.publish("hyper_params/resolution",
            json.dumps(image_capture_params))
        print(image_capture_params) 

    @route('/speed_and_angle', method = 'POST')
    def process_data():
        #extract data from POST
        angle = request.forms.get('angle') #in degrees
        speed = request.forms.get('speed') #in km/h
        print(speed,angle)
        #process html form and publish data to mqtt
        client.publish("command/wheel_speed", speed) #publish to speed
        client.publish("command/steering", angle) #publish to steering

    @get('/get_sensor_data')
    def return_sensor_data():
        values_dict = grab_data(sensor_data)#grabs values from the data grab function
        return(json.dumps(values_dict))
        
    @get('/algorithm_outputs')
    def return_algorithm_outputs():
        dump = {
            'rpm' : current_vals[0],
            'current_distance' : current_vals[1],
            'current_angle' : current_vals[2]}
        return(json.dumps(dump))

    @route('/off', method="POST")
    def off(): 
        client.publish("command/wheel_speed", 0)

    run(host='0.0.0.0', port=8080, debug = True) #starts a built-in dev server
    
if __name__ == '__main__':
    #connects and starts mqtt client
    client = mqtt_connect()
    #declaring a global arrays for sensor_data
    sensor_data = [0] * 6
    #empty dictionary for the returned algorithm values
    current_vals = [0] * 3
    try:
        client.loop_start()
        #waiting for connection
        time.sleep(0.1)
        add_call_backs(client) #adds callback functions for each topic
        #function for subscribing to the main MQTT telemety topic
        client.subscribe('telemetry/#')
        client.subscribe('program_outputs/#')
        #starts webserver
        web_server()

    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()
        sys.stderr.close()
