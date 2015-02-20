#!/usr/bin/python2
import Image, ImageDraw
from sys import argv
from imageprocessing import openImage
import colorsys
from random import uniform

def center(x, y):
   xmed = sum(x)/len(x)
   ymed = sum(y)/len(y)
   return xmed, ymed

def color():
   hsv = uniform(0, 1), 1.0, 1.0
   r, g, b = colorsys.hsv_to_rgb(*hsv)
   return int(r*255), int(g*255), int(b*255)

def drawbox(newimage, figure):
   x = []
   y = []
   for i in figure:
      x.append(i[0])
      y.append(i[1])
   minx = min(x)
   miny = min(y)
   maxx = max(x)
   maxy = max(y)
   draw = ImageDraw.Draw(newimage)
   col = color()
   draw.rectangle((minx, miny, maxx, maxy), outline = col)
   c = center(x, y)
   draw.point(c, fill = col)
   return newimage

def dfs((x, y), pixels, visited, width, height):
   s = []
   s_visited = []
   s.append((x, y))
   while len(s) > 0:
      cur = s.pop()
      if cur not in s_visited and cur not in visited:
         for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
               nb = (cur[0]+i, cur[1]+j)
               if nb[0] >= 0 and nb[1] >= 0 and nb[0] < width-1 and nb[1] < height-1:
                  if pixels[nb] != (0, 0, 0):
                     s.append(nb)
         s_visited.append(cur)
   return s_visited

def detectshapes(image):
   pixels = image.load()
   width, height = image.size
   newimage = image.copy()
   visited = []
   nshapes = 0
   i=0
   for x in xrange(0, width):
      for y in xrange(0, height):
         if pixels[x, y] != (0, 0, 0):
            i+=1
         if (x, y) not in visited and pixels[x, y] != (0, 0, 0):
            nshapes += 1
            print "nshapes", nshapes
            s_visited = dfs((x, y), pixels, visited, width, height)
            newimage = drawbox(newimage, s_visited)
            visited.extend(s_visited)
         visited.append((x, y))
   print i
   newimage.save('newimage2.png')
   print len(visited)
   print width, height, width*height, nshapes

if __name__=='__main__':
   try:
      image = Image.open(argv[1])
   except:
      image = openImage()
   detectshapes(image)
