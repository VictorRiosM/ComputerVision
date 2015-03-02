#!/usr/bin/python2
import edgedetector
from imageprocessing import openImage
from sys import argv
import Image
from math import radians, cos, sin, pi

def drawimage(image, data, mostvoted):
   width, height = image.size
   newimage = image.copy()
   for x in xrange(0, width):
      for y in xrange(0, height):
         ang, rho = data[x][y]
         if (ang, rho) in mostvoted and sin(ang)!=0:
            ycoord = (-cos(ang)/sin(ang))*x + rho/sin(ang) # Equation
            if ycoord >= 0 and ycoord < height:
               newimage.putpixel((x, int(ycoord)), (255, 0, 0))
   newimage.save('newimage.png')
   newimage.show()

def linedetection(image, magnitudes, angle):
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
            ydata.append((orad, rho))
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

   mostvoted = list()
   for pair in pairs:
      if pair is not (None, None): #and pairs[pair] > 2:
         mostvoted.append(pair)
   drawimage(image, data, mostvoted)


try:
   image = Image.open(argv[1])
except:
   image = openImage()
magnitudes, angles = edgedetector.edgedetection(image)
linedetection(image, magnitudes, angles)
