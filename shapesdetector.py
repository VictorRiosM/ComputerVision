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

# color() returns a random color
def color():
   # The hue value is randomized
   hsv = uniform(0, 1), 1.0, 1.0
   r, g, b = colorsys.hsv_to_rgb(*hsv)
   return int(r*255), int(g*255), int(b*255)

# Draw the bounding box and get the mass center
def drawbox(newimage, figure, col):
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
   draw.rectangle((minx, miny, maxx, maxy), outline = col)
   c = center(x, y)
   draw.point(c, fill = col)
   return newimage

# The depth first search subroutine
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
               if nb[0] >= 0 and nb[1] >= 0 and nb[0] < width and nb[1] < height:
                  if pixels[nb] == (255, 255, 255):
                     s.append(nb)
         s_visited.append(cur)
   return s_visited

def floodfill(pixels, p, width, height):
   s = []
   newcolor = color()
   if pixels[p] != (0, 0, 0):
      return pixels, None
   s.append(p)
   while len(s) != 0:
      p = s.pop()
      if pixels[p] == (0, 0, 0):
         pixels[p] = newcolor
         x, y = p
         if x-1>=0 and pixels[x-1, y] == (0, 0, 0):
            s.append((x-1, y))
         if x+1<width and pixels[x+1, y] == (0, 0, 0):
            s.append((x+1, y))
         if y-1>=0 and pixels[x, y-1] == (0, 0, 0):
            s.append((x, y-1))
         if y+1<height and pixels[x, y+1] == (0, 0, 0):
            s.append((x, y+1))
   return pixels, newcolor

def detectshapes(image, path):
   pixels = image.load()
   width, height = image.size
   
   colors = []
   for x in xrange(0, width):
      for y in xrange(0, height):
         pixels, color = floodfill(pixels, (x, y), width, height)
         if color != None:
            colors.append(color)
   i = Image.new('RGB', (width, height))
   for x in xrange(0, width):
      for y in xrange(0, height):
         i.putpixel((x, y), pixels[x, y])
   #i.save('Shapesdetection/floodfill.png')
   
   # New image to show the result   
   visited = [] # List to save the visited pixels
   nshapes=0
   for x in xrange(0, width):
      for y in xrange(0, height):
         # Detect shape by edges
         if (x, y) not in visited and pixels[x, y] == (255, 255, 255):
            nshapes += 1
            # The dfs subroutine returns the shape edge pixels
            s_visited = dfs((x, y), pixels, visited, width, height)
            # Draw the box and the mass center
            i = drawbox(i, s_visited, colors[nshapes+1])
            visited.extend(s_visited)
         visited.append((x, y))
   #newimage.save(path)
   i.save(path)

if __name__=='__main__':
   try:
      image = Image.open(argv[1])
   except:
      image = openImage()
   try:
      path = argv[2]
   except:
      path = 'Shapesdetection/image2.png'
   detectshapes(image, path)
