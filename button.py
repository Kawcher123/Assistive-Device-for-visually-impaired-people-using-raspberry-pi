from PIL import Image
from gtts import gTTS

# ocr import
import os
import pytesseract
import subprocess
import picamera

#switch import
import RPi.GPIO as GPIO
import time
import imutils
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

serial = 1;    
def call_OCR():
    print("take picture")
    with picamera.PiCamera() as camera:
        camera.resolution = (1080,720)
        #camera.framerate=15
        #camera.brightness=100
        camera.rotation = -90
        camera.capture("/home/pi/Desktop/switch/p"+serial+".png")
        serial+=1
    print("taken")
    print(serial)

    #im = Image.open("p1.png")
    #im=imutils.rotate(im,angle=90)
    #im=im.convert('1')
    #im.save('p1.png')
     
    #text_ocr = pytesseract.image_to_string(im, lang = 'eng')
    #print(text_ocr)


    #text2speech = gTTS(text=text_ocr,lang='en')
    #text2speech.save("sample.mp3")
    #os.system("mpg321 sample.mp3")

while True:
    if GPIO.input(11):
        print("Clicked for text to speech")
       # try:
            #call_OCR()
       # except:
         #   print("error occured in image")
    elif GPIO.input(13):
        print("Clicked for text to object detection")
    else:
        print("No click")
    time.sleep(1)

