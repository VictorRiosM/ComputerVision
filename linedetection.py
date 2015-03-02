#!/usr/bin/python2
import edgedetector
from imageprocessing import openImage
from sys import argv
import Image
import math


def linedetection(image, magnitudes, angle):
   pixels = image.load()
   width, height = image.size
   edges = list()
   i=0
   for x in xrange(0, width):
      for y in xrange(0, height):
         if angle[i] is not None:
            orad = math.radians(angle[i])
            rho = (x*math.cos(orad) + y*math.sin(orad))
            edges.append((orad, rho))
         else:
            edges.append((None, None))
         i+=1

   # Including background
   pairs={}
   for i in xrange(0, len(edges)):
      pair = (edges[i])
      if pair in pairs:
         pairs[pair] += 1
      else:
         pairs[pair] = 1





try:
   image = Image.open(argv[1])
except:
   image = openImage()
magnitudes, angles = edgedetector.edgedetection(image)
linedetection(image, magnitudes, angles)
