from bottle import Bottle, route, run, static_file, debug, template, request
import paho.mqtt.client as mqtt
import time
import json

#create function for callback
def on_publish(client,userdata,result):             
    print("data published \n")
    pass

#connecting to mqtt
broker="localhost"
client = mqtt.Client() #create client object
client.on_publish = on_publish #assign function to callback
client.connect(broker) #establish connection

#Bottle code
debug(True)
@route('/controldash') #binds a piece of code to a url path
def send_site():
    #function will serve up the control dashboard html page
    return template('./controldash.tpl')

@route('/js/jquery.min.js')
def send_jquery():
    return static_file('/jquery.min.js', root = './js')

@route('/killed', method = 'POST')
def send_killed():
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
    #need to create a dict after usng the request.forms.get then make the dict into a json before mqtt publish
    #decision_params = json.dump
    #client.publish("hyper_params/decision", )

@route('/hyper_params/image_processing', method = 'POST')
def send_image_processing_params():

    #client.publish('hyper_params/image_processing')

@route('/hyper_params/image_capture', method = 'POST')   
def send_image_capture_params():

    #client.publish()

@route('/speed_and_angle', method = 'POST')
def process_data():
    #extract data from POST
    angle = request.forms.get('angle') #in degrees
    speed = request.forms.get('speed') #in km/h
    print(speed,angle)
    #process html form and publish data to mqtt
    client.publish("command/wheel_speed", speed, retain = True) #publish to speed
    client.publish("command/steering", angle, retain = True) #publish to steering
            

run(host='localhost', port=8080, debug = True) #starts a built-in dev server