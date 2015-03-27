#!/usr/bin/python2
import edgedetector
from imageprocessing import openImage
from sys import argv
import Image, ImageDraw
from math import radians, cos, sin, pi
from cv_lab.colors import color


def drawline(image, line, data):
   width, height = image.size
   c = color()
   for y in xrange(0, height):
      for x in xrange(0, width):
         if line[0] != 0:
            ycoord = (-cos(line[0])/sin(line[0]))*x + line[1]/sin(line[0])
            if ycoord >= 0 and ycoord < height:
               image.putpixel((x, int(ycoord)), c)
   image.save('newimage.png')


def linedetection(image):
   magnitudes, angle = edgedetector.edgedetection(image)
   pixels = image.load()
   width, height = image.size
   data = list()
   i=0
   for x in xrange(0, width):
      ydata = list()
      for y in xrange(0, height):
         if angle[i] is not None:
            orad = radians(angle[i])%pi
            rho = (x*cos(orad) + y*sin(orad))
            ydata.append((float('%.2f' % orad), float('%.f' % rho)))
            
         else:
            ydata.append((None, None))
         i+=1
      data.append(ydata)

   pairs = dict()
   for x in xrange(0, width):
      for y in xrange(0, height):
         if x>0 and x<width-1 and y>0 and y<height-1:
            ang, rho = data[x][y]
            if ang is not None:
               pair = (data[x][y])
               if pair in pairs:
                  pairs[pair] += 1
               else:
                  pairs[pair] = 1
   
#   print pairs.values()
   lines = list()
   for pair in pairs:
      if pairs[pair] > 1:
         lines.append(pair)

   for line in lines:
      drawline(image, line, data)
   
   return lines, data



try:
   image = Image.open(argv[1])
except:
   image = openImage()
lines, data = linedetection(image)
