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
#gray = cv2.imread(args["image"], 0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gis", gray)

ret, thresh = cv2.threshold(gray, 50, 255, 1)
kernel = np.ones((3,3),np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)


thresh = cv2.dilate(thresh, kernel, iterations = 15)
thresh = cv2.erode(thresh, kernel, iterations = 15)

cv2.imshow("tresh", thresh)
countours, h ,d = cv2.findContours(thresh, 1, 2)
for cnt in h:
    epsilon = cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    print len(approx)
    M = cv2.moments(cnt)
    area = cv2.contourArea(cnt)

    if len(approx == 4) and (area > 4500):
        print "square"
        print area
        cv2.drawContours(image,[cnt],0,(0,0,255),-1)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(image, (cx,cy), 5, (0,255,0))
cv2.imshow('holi', image)

# find the colors within the specified boundaries and apply
# the mask

# show the images 
cv2.waitKey(0)
