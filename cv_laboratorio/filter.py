#!/usr/bin/python2
import Image
from imageprocessing import openImage
from sys import argv

def filter(image, fil='median', nbh='8'):
   
   image.convert("RGB")
   pixels = image.load()
   width, height = image.size
   #newimage = Image.new('RGB', (width, height))

   # Filter by median
   if fil=='median':
      if nbh=='8':
         for x in xrange(0, width):
            for y in xrange(0, height):
               rlist = []
               glist = []
               blist = []
               for i in [-2, 0, 2]:
                  for j in [-2, 0, 2]:
                     if x+i>=0 and x+i<width and y+j>=0 and y+j<height:
                        r, g, b = pixels[x+i, y+j]
                        rlist.append(r)
                        glist.append(g)
                        blist.append(b)
               rmedian = sum(rlist)/len(rlist)
               gmedian = sum(glist)/len(glist)
               bmedian = sum(blist)/len(blist)
               #newimage.putpixel((x, y), (rmedian, gmedian, bmedian))
               pixels[x, y] = (rmedian, gmedian, bmedian)

   # The minimum value
   elif fil=='min':
      if nbh=='8':
         for x in xrange(0, width):
            for y in xrange(0, height):
               rlist = []
               glist = []
               blist = []
               for i in [-1, 0, 1]:
                  for j in [-1, 0, 1]:
                     if x+i>=0 and x+i<width and y+j>=0 and y+j<height:
                        r, g, b = pixels[x+i, y+j]
                        rlist.append(r)
                        glist.append(g)
                        blist.append(b)
               rmin = min(rlist)
               gmin = min(glist)
               bmin = min(blist)
               newimage.putpixel((x, y), (rmin, gmin, bmin))

   # The maximum value
   elif fil=='max':
      if nbh=='8':
         for x in xrange(0, width):
            for y in xrange(0, height):
               rlist = []
               glist = []
               blist = []
               for i in [-1, 0, 1]:
                  for j in [-1, 0, 1]:
                     if x+i>=0 and x+i<width and y+j>=0 and y+j<height:
                        r, g, b = pixels[x+i, y+j]
                        rlist.append(r)
                        glist.append(g)
                        blist.append(b)
               rmax = max(rlist)
               gmax = max(glist)
               bmax = max(blist)
               pixels[x, y] = (rmax, gmax, bmax)

   #newimage.save('newimage.png')
   #newimage.show()
   return pixels

if __name__=='__main__':
   try:
       # Call filter with image and filter as args
      image = Image.open(argv[1])
      filter(image, argv[2], argv[3])
   except:
      filter(openImage())
