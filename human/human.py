import numpy as np
import cv2
from matplotlib import pyplot as plt
import imutils
from PIL import Image
from picamera import PiCamera
import pyttsx3


faceCascade=cv2.CascadeClassifier("/home/pi/Desktop/switch/human/haarcascade_upperbody.xml")
cam = PiCamera()
cam.resolution = (1080, 720)
cam.framerate = 32
cam.rotation = 90
cam.brightness=70
minW = 0.1*640
minH = 0.1*480
while True:
    
    cam.capture("/home/pi/Desktop/switch/human/face1.png")
    #img = np.asarray(Image.open("/home/pi/Desktop/switch/human/face1.png"))
    img =cv2.imread("/home/pi/Desktop/switch/human/face1.png")
    img = cv2.flip(img, -1) # Flip vertically
    img=imutils.rotate(img,angle=180)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    body = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in body:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        r=(2*x+w)/2
        if r>640:
            engine = pyttsx3.init()
            engine.say("Go left")
            engine.runAndWait()
            print("right")
        else:
            engine = pyttsx3.init()
            engine.say("Go right")
            engine.runAndWait()
            print("left")

    cv2.imshow("detect",img)
    if cv2.waitKey(1) & 0xff==ord("q"):
        break
cv2.destroyAllWindows()
