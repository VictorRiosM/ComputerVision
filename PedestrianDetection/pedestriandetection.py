#!/usr/bin/python2
import numpy as np
from sys import argv
import cv2
import os
import imp

colorsfile = imp.load_source('colors', '../cv_laboratorio/colors.py')

try:
    cap = cv2.VideoCapture(argv[1])
except:
    cap = cv2.VideoCapture('/home/victor/TownCentreXVID.avi')

fgbg = cv2.BackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

while (1):
    
    #trainingSetPositive = 'training/positive/'
    #trainingSetNegative = 'training/negative/'
 
    #positives = os.listdir(trainingSetPositive)
    #negatives = os.listdir(trainingSetNegative)

    #print "Positives", positives
    #print "Negatives", negatives

    ret, img = cap.read()

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
    k = cv2.waitKey(30) & 0xff                                                                                                                      
    if k == 27:                                                                                                                                      
       break     
    exit
    
# fgbg = cv2.BackgroundSubtractorMOG2()
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# while(1):
#     # Get frame
#     ret, frame = cap.read()
    
#     # Gaussian filter
#     blur = cv2.GaussianBlur(frame, (3,3), 0)
    
#     # Apply background subtractor
#     fgmask = fgbg.apply(blur, None, 0.005)
    
#     fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

#     # Show
#     cv2.imshow('blur', blur)
#     cv2.imshow('fgmask', fgmask)

#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break


# cap.release()
# cv2.destroyAllWindows()

