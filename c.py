from __future__ import print_function
import imutils
from imutils.video import VideoStream
#import imutils
import time
import cv2
import os
from gtts import gTTS
from picamera.array import PiRGBArray
from picamera import PiCamera



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
camera.resolution = (640, 480)
camera.framerate = 32
camera.brightness=50
rawCapture = PiRGBArray(camera, size=(640, 480))
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
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            # position Servo at center of circle
            mapObjectPosition(int(x), int(y))
            
            



    # show the frame to our screen
    cv2.imshow("Frame", frame)
    
    # if [ESC] key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
            break

# do a bit of cleanup
print("\n Exiting Program and cleanup \n")
cv2.destroyAllWindows()
vs.stop()
