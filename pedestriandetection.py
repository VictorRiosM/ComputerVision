#!/usr/bin/python2

import numpy as np
import cv2
from sys import argv

try:
    cap = cv2.VideoCapture(argv[1])
except:
    cap = cv2.VideoCapture(0)

fgbg = cv2.BackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame, None, 0.005)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('frame', frame)
    cv2.imshow('fgmask', fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
