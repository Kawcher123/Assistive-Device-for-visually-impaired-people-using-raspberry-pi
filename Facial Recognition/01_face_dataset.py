''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    
  
'''

import cv2
import os
import imutils
from PIL import Image
import numpy as np
from picamera import PiCamera

#cam = cv2.VideoCapture(0)
#cam.set(3, 640) # set video width
#cam.set(4, 480) # set video height

# initialize the camera and grab a reference to the raw camera capture
cam = PiCamera()
cam.resolution = (1080, 720)
cam.framerate = 32
cam.rotation = 90
cam.brightness=50

face_detector = cv2.CascadeClassifier('/home/pi/Desktop/switch/FacialRecognitionProject/haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):
    cam.capture("/home/pi/Desktop/switch/FacialRecognitionProject/face.png")
    #img = np.asarray(Image.open("/home/pi/Desktop/switch/FacialRecognitionProject/face.png"))
    img = cv2.imread("/home/pi/Desktop/switch/FacialRecognitionProject/face.png")
    img = cv2.flip(img, -1) # flip video image vertically
    print("Captured:yes")
    img=imutils.rotate(img,angle=180)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
    cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    print("count:%",count)
    if k == 27:
        break
    elif count >= 100: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")

cv2.destroyAllWindows()

