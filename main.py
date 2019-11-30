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


while True:
    if (GPIO.input(13) and GPIO.input(15)):
        print("Press for Objectect detection")
        call(["python3","/home/pi/tensorflow1/models/research/object_detection/Object_detection_picamera.py"])
    elif GPIO.input(11):
        print("Press for text to speech")     
        try:
            call(["python3","tts.py"])
        except:
            print("error occured in OCR")
    elif GPIO.input(13):
        print("Press for Face recognition")
        try:
            print("call")
            call(["python3","faceRecognition.py"])
        except:
            print("error occured in Face recognition")
    elif GPIO.input(15):
        print("Press for yellow path")
        try:
            print("call")
            call(["python3","yellowPath.py"])
        except:
            print("error occured in yellow path")
    else:
        print("No click")
    time.sleep(1)

