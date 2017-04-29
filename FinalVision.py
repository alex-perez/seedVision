import numpy as np
import cv2
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

def takePhoto():
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/control/picamera.jpg')
    camera.stop_preview()

# construct the argument parse and parse the arguments
salidaCorrecta = 27
entradaCam = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(salidaCorrecta, GPIO.OUT)

camera = PiCamera()



#while True:
# load the image
#ret, image = video_capture.read()
takePhoto()
image = cv2.imread("picamera.jpg")
image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

blur = cv2.GaussianBlur(image, (5,5), 0)
seedCnt = 0

low_hsv = np.array([18,59,120])
high_hsv = np.array([180,255,255])
mask = cv2.inRange(hsv, low_hsv, high_hsv)
kernel = np.ones((1,1), np.uint8)
mask = cv2.erode(mask, kernel, iterations = 1)
res = cv2.bitwise_and(image, image, mask=mask)
contours, h, d = cv2.findContours(mask, 1,2)
for cnt in h:
    M = cv2.moments(cnt)
    area = cv2.contourArea(cnt)
    if area > 30:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(image, (cx,cy), 5, (0,55,200))
        cv2.circle(res, (cx,cy), 5, (0,55,200))
        seedCnt += 1

if seedCnt >= 12:
    print "aceptable"
    GPIO.output(salidaCorrecta, GPIO.HIGH)
else:
    print "no aceptable"
    GPIO.output(salidaCorrecta, GPIO.LOW)

cv2.imshow('mask', mask)
cv2.imshow('original', image)
cv2.imshow('res', res)
#if cv2.waitKey(1) & 0xFF == ord('q'):
    #break
cv2.waitKey(0)
print seedCnt
sleep(15)
GPIO.cleanup()
cv2.destroyAllWindows()
