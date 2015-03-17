#!/usr/bin/python2
import colorsys
from random import uniform

def color():
   hsv = uniform(0, 1), 1.0, 1.0
   rgb = colorsys.hsv_to_rgb(*hsv)
   r = int(rgb[0]*255)
   g = int(rgb[1]*255)
   b = int(rgb[2]*255)
   return r, g, b

r, g, b = color()
