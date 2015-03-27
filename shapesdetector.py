#!/usr/bin/python2
import Image, ImageDraw
from sys import argv
from imageprocessing import openImage
import colorsys
from random import uniform

# Bounding box center
def boxcenter(x, y):
   xmed = sum(x)/len(x)
   ymed = sum(y)/len(y)
   return xmed, ymed

# Mass center
def getmasscenter(shape):
   x = []
   y = []
   for p in shape:
      x.append(p[0]) 
      y.append(p[1])
   xprom = sum(x)/len(x)
   yprom = sum(y)/len(y)
   return xprom, yprom

# Returns a random color
def color():
   # The hue value is randomized
   hsv = uniform(0, 1), 1.0, 1.0
   r, g, b = colorsys.hsv_to_rgb(*hsv)
   return int(r*255), int(g*255), int(b*255)

# Draw the bounding box and the mass center
def drawbox(newimage, figure, col, mcenter):
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
   # Mass center Black
   draw.point(mcenter, fill = 'black')
   # Bounding box center Yellow
   draw.point(boxcenter(x, y), fill = 'yellow')
   return newimage

def getpercentage(shape, width, height):
   return 100.0/float(width*height) * len(shape)

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

#Floodfill subroutine
# Fills every shape with a different color
def floodfill(pixels, p, width, height):
   s = []
   newcolor = color()
   if pixels[p] != (0, 0, 0):
      return pixels, None, None
   s.append(p)
   shape = []
   while len(s) != 0:
      p = s.pop()
      if pixels[p] == (0, 0, 0):
         pixels[p] = newcolor
         shape.append(p)
         x, y = p
         # 4-neighborhood, (0, 0, 0) means that the pixel has not been filled
         if x-1>=0 and (pixels[x-1, y] == (0, 0, 0) or pixels[x-1, y] == (255, 255, 255)):
            s.append((x-1, y))
         if x+1<width and (pixels[x+1, y] == (0, 0, 0) or pixels[x+1, y] == (255, 255, 255)):
            s.append((x+1, y))
         if y-1>=0 and (pixels[x, y-1] == (0, 0, 0) or pixels[x, y-1] == (255, 255, 255)):
            s.append((x, y-1))
         if y+1<height and (pixels[x, y+1] == (0, 0, 0) or pixels[x, y+1] == (255, 255, 255)):
            s.append((x, y+1))
   return pixels, newcolor, shape

def getshapes(width, height, pixels):
   i = Image.new('RGB', (width, height))
   for x in xrange(0, width):
      for y in xrange(0, height):
         i.putpixel((x, y), pixels[x, y])
   visited = [] # List to save the visited pixels
   nshapes = 0
   shapes = []
   for x in xrange(0, width):
      for y in xrange(0, height):
         # Detect shape by edges
         if (x, y) not in visited and pixels[x, y] == (255, 255, 255):
            nshapes += 1
            # The dfs subroutine returns the shape edge pixels
            s_visited = dfs((x, y), pixels, visited, width, height)
            # Draw the box and the mass center
            #i = drawbox(i, s_visited, colors[nshapes], mcenters[nshapes])
            shapes.append(s_visited)
            visited.extend(s_visited)
         visited.append((x, y))
   return nshapes, shapes

# The main subroutine for shapedetection
def detectshapes(image, path):
   pixels = image.load()
   width, height = image.size

   # Data received from the floodfill
   colors = []
   mcenters = []
   percentages = []
   # Apply floodfill
   for x in xrange(0, width):
      for y in xrange(0, height):
         pixels, color, shape = floodfill(pixels, (x, y), width, height)
         if color != None:
            colors.append(color)
         if shape != None:
            mcenters.append(getmasscenter(shape))
            percentages.append(getpercentage(shape, width, height))
   
   nshapes, shapes = getshapes(width, height, pixels, colors)

   i.save(path)
   pbgcolor = max(percentages)
   for n in xrange(0, nshapes):
      if percentages[n] == pbgcolor:
         print "Element:", n, "Color:", colors[n], "Percentage:", percentages[n], "Probably this is the background"
      else:
         print "Element:", n, "Color:", colors[n], "Percentage:", percentages[n]



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
