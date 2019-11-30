from PIL import Image
from gtts import gTTS

# ocr import
import os
import pytesseract
import subprocess
import picamera
import numpy as np
import cv2
import pyttsx3
import pyTTS
#switch import
import RPi.GPIO as GPIO
import time
import imutils
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)




#src_path = "/home/pi/Desktop/switch/"


    
def speechCall(text_ocr):
    '''text2speech = gTTS(text=text_ocr,lang='en')
    text2speech.save("sample.mp3")
    os.system("mpg321 sample.mp3")
    engine = pyttsx3.init()
    engine.getProperty('rate')
    engine.setProperty('rate',70)
    engine.say(text_ocr)
    engine.runAndWait()'''
    tts=pyTTS.Create()
    tts.Speak(text_ocr)
speechCall("Create an account or log into Facebook. Connect with friends, family and other people you")


