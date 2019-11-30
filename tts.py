from PIL import Image
from gtts import gTTS

# ocr import
import os
import pytesseract
import subprocess
from subprocess import call
import picamera
import numpy as np
import cv2
import pyttsx3
import datetime
#switch import
import RPi.GPIO as GPIO
import time
import imutils
from picamera import PiCamera
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)



src_path = "/home/pi/Desktop/switch/"

def captureImage():
    print("take picture")
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.resolution = (1080,720)
        #camera.framerate=15
        camera.brightness=60
        camera.rotation = 90
        camera.capture('/home/pi/Desktop/switch/p1.png')
        time.sleep(1)
        camera.capture('/home/pi/Desktop/switch/p2.png')
        time.sleep(1)
        camera.capture('/home/pi/Desktop/switch/p3.png')
        camera.start_preview()
    print("taken")


 
def get_string(img_path):
    #print("yes1 "+img_path)
    # Read image with opencv
    img = cv2.imread(img_path)
    print("read image: yes")
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
 
    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", img)
 
    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
 
    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", img)
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))
 
    # Remove template file
    #os.remove(temp)
 
    return result
    
    
def speechCall(text_ocr):
    '''text2speech = gTTS(text=text_ocr,lang='en')
    text2speech.save("sample.mp3")
    os.system("mpg321 sample.mp3")'''
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english+f3')  # changes the voice
    engine.setProperty('rate', 125)  
    engine.say(text_ocr)     
    engine.runAndWait()



captureImage()
print("Captured image")
text_ocr1 = get_string(src_path + "p3.png")
if len(text_ocr1)!=0:
    print(text_ocr1)
    speechCall(text_ocr1)
else:
    print("No text in image 3")
    text_ocr2 = get_string(src_path + "p2.png")
    print(text_ocr2)
    if len(text_ocr2)!=0:
        speechCall(text_ocr2)

