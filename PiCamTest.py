
import picamera
import time
import RPi.GPIO as gpio
import numpy as np
import os

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(12, gpio.OUT)

gpio.setup(15, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(21, gpio.OUT)
gpio.setup(22, gpio.OUT)

gpio.output(11, True)
gpio.output(12, True)
gpio.output(15, True)
gpio.output(16, True)
gpio.output(21, True)
gpio.output(22, True) 

def capture_CV(image,camera):
    camera.capture(image,'bgr', use_video_port = True)

def enableA():
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    os.system(i2c)
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(12, True)

def enableC():
    i2c = "i2cset -y 1 0x70 0x00 0x06"
    os.system(i2c)
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(12, False)

def initializeCamera(camera,resolution):
    camera.resolution = (resolution, resolution)
    camera.framerate = 24

    enableA()
    camera.start_preview()
    time.sleep(2)

    enableC()
    camera.start_preview()
    time.sleep(2)

def main():
    camera = picamera.PiCamera()
    resolution = 128
    initializeCamera(camera,resolution)
    
    start = time.time()
    image = np.empty((resolution**2*3,),dtype = np.uint8)
    
    enableA()
    capture_CV(image,camera)
    
    enableC()
    capture_CV(image,camera)
    
    print(time.time()-start)
    
    camera.stop_preview()
    camera.close()
    
if __name__ == "__main__":
    main()

    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(12, True)

