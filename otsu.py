import numpy as np
import argparse
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
#image = cv2.imread("seed1.jpg")
image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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


cv2.imshow('mask', mask)
cv2.imshow('original', image)
cv2.imshow('res', res)

print seedCnt
cv2.waitKey(0)
