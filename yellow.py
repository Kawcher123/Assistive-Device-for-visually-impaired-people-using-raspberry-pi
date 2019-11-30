from __future__ import print_function
import imutils
from imutils.video import VideoStream
import imutils
import time
import cv2
import os
from gtts import gTTS
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import matplotlib.pyplot as plt



# print object coordinates
def mapObjectPosition (x, y):
    print ("Object Center coordenates at X0 = {0} and Y0 =".format(x))
    if x==320:
        #text2speech=gTTS("you are in the middle",lang="en")
        #text2speech.save("obj.mp3")
        os.system("mpg321 obj.mp3")

# initialize the video stream and allow the camera sensor to warmup
print(" waiting for camera to warmup...")
#usingPiCamera=True
#frameSize=(320,240)
#vs = VideoStream(src=0,usePiCamera=usingPiCamera,resolution=frameSize,framerate=32).start()
#time.sleep(2.0)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1080, 720)
camera.framerate = 32
camera.brightness=50
camera.rotation = 90
rawCapture = PiRGBArray(camera, size=(1080,720))
time.sleep(.5)


# define the lower and upper boundaries of the object
# to be tracked in the HSV color space
#colorLower = (18, 45, 196)
#colorUpper = (45, 255, 255)
colorLower = (24,100,100)
colorUpper = (44,255,255)
#colorUpper = (71, 234, 213)

# loop over the frames from the video stream
for imageArray in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the next frame from the video stream, Invert 180o, resize the
    # frame, and convert it to the HSV color space
    #time.sleep(1.0)
    frame = imageArray.array
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    print(np.shape(frame))

    """
    frame = vs.read()
    if not usingPiCamera:
        frame = imutils.resize(frame, width=500)
        frame = imutils.rotate(frame, angle=360)"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the object color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res=cv2.bitwise_and(frame,frame,mask=mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        x,y,w,h=cv2.boundingRect(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        r=2*x+w

        # only proceed if the radius meets a minimum size
        if r > 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x), int(y)), int(radius),
                #(0, 255, 255), 2)
            cv2.rectangle(res,(x,y),(x+w,y+h),(45,255,255),2)
            cv2.circle(res, center, 5, (0, 0, 255), -1)
            
            # position Servo at center of circle
            mapObjectPosition(int((2*x+w)/2), int((2*y+h)/2))
            pixel=frame[200,550]
            #print(pixel)
            #r=[]
            #g=[]
            #b=[]
            #rows,cols=np.shape(frame)
            #framed=np.asarray(frame)
            #rows,cols=framed.shape
            for i in range(720):
                for j in range(1080):
                    r=res[i,j,0]
                    g=res[i,j,1]
                    b=res[i,j,2]
                    print("r=",r)
                    print("g=",g)
                    print("b=",b)
                    #k=(r,g,b)
                    if (r==45 and g==255 and b==255):
                        x1=i
                        y1=j
                        print('x= ',x1)
                        print('y=',y1)
                        plt.plot(x1,y1)
                        plt.show()
                        
                    else:
                        break
                
                    
            



    # show the frame to our screen
    cv2.imshow("Frame", res)
    
    # if [ESC] key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
            break

# do a bit of cleanup
print("\n Exiting Program and cleanup \n")
cv2.destroyAllWindows()
vs.stop()
