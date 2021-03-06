#!/usr/bin/python2
import edgedetector, linedetection
from imageprocessing import openImage
from sys import argv
import Image, ImageDraw
from math import radians, cos, sin, pi
from colors import color

def drawcircle(image, (xc, yc), radius):
    draw = ImageDraw.Draw(image)
    c = color()
    draw.ellipse((xc - radius, yc - radius, xc + radius, yc + radius), outline=c)
    image.save("newimage.png")

def circledetection(image, magnitudes, angles, radius, lines, data):
   width, height = image.size
   if radius != None:
       for line in lines:
          xcenter=dict()
          ycenter=dict()
          for x in xrange(0, width):
             for y in xrange(0, height):
                xc = x - radius*cos(line[0])
                yc = y - radius*sin(line[0])
                if xc in xcenter:
                   xcenter[xc] += 1
                else:
                   xcenter[xc] = 1
                if yc in ycenter:
                   ycenter[yc] += 1
                else:
                   ycenter[yc] = 1
                mostfrequentx = max(xcenter.values())
                mostfrequenty = max(ycenter.values())
       
          for x in xcenter:
             if xcenter[x] == mostfrequentx:
                xc = x
          for y in ycenter:
             if ycenter[y] == mostfrequenty:
                yc = y
          drawcircle(image, (xc, yc), radius)
        

try:
   image = Image.open(argv[1])
except:
   image = openImage()
try:
   radius = int(argv[2])
except:
   radius = None
magnitudes, angles = edgedetector.edgedetection(image)
lines, data = linedetection.linedetection(image)
circledetection(image, magnitudes, angles, radius, lines, data)
