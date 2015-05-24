#!/usr/bin/python2
import numpy as np
from sys import argv
import cv2
import os
import imp
# Import colors
colorsfile = imp.load_source('colors', '../cv_laboratorio/colors.py')

# Get image or video

try:
    cap = cv2.VideoCapture(argv[1])
except:
    cap = cv2.VideoCapture('/home/victor/TownCentreXVID.avi')


# Initialize background subtractor
#fgbg = cv2.BackgroundSubtractorMOG2()
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))


#############################################

# Select Region of Interest
# Based on Capturing mouse click events with Python and OpenCV by Adrian Rosebrock
# http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/

roi = list()

def selectROI(event, x, y, flags, params):
    global roi
    
    if event == cv2.EVENT_LBUTTONUP:
        roi.append((x, y))
        if len(roi) == 2:
            cv2.rectangle(img, roi[0], roi[1], (255, 0, 0), 2)


ret, img = cap.read()
backup = img.copy()
cv2.namedWindow("SelectROI")
cv2.setMouseCallback("SelectROI", selectROI)

while True:
    cv2.imshow("SelectROI", img)
    k = cv2.waitKey(10) &0xFF

    if k == ord('z'):
        img = backup.copy()
        roi = []

    if k == 27:
        break



print roi
#############################################

# Detect People

while True:
    
    #trainingSetPositive = 'training/positive/'
    #trainingSetNegative = 'training/negative/'
 
    #positives = os.listdir(trainingSetPositive)
    #negatives = os.listdir(trainingSetNegative)

    #print "Positives", positives
    #print "Negatives", negatives

    try:
        ret, img = cap.read()
        img = img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
    except:
        exit(1)

    # Background subtraction
    #blur = cv2.GaussianBlur(img, (3,3), 0)
    #fgmask = fgbg.apply(img, None, 0.5)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
    #img = cv2.imread(trainingSetPositive+positives[0])

    # HOG Descriptor
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'winStride': (0, 0), 'padding': (0, 0), 'scale': 1.05}
    #found = hog.detect(img)
    found = hog.detectMultiScale(img, **hogParams);
    
    noofpersons = len(found[0])

    # Different colors
    col = colorsfile.color(noofpersons)

    # Bounding box
    for i in xrange(0, noofpersons):
        person = found[0][i].tolist()
        x=person[0]
        y=person[1]
        xf=person[0]+person[2]
        yf=person[1]+person[3]
        cv2.rectangle(img, (x, y), (xf, yf), col[i], 1)

    cv2.putText(img, "Number of persons: " + str(noofpersons), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show results
    cv2.imshow("people detector", img)
    k = cv2.waitKey(10) & 0xff                            
    if k == 27:                                                                                                                       
       break
    
cap.release()
cv2.destroyAllWindows()
