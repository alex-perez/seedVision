# import the necessary packages
import numpy as np
import argparse
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
image = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
cv2.imshow('holi', image)

# find the colors within the specified boundaries and apply
# the mask

# show the images 
cv2.waitKey(0)
