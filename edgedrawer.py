#!/usr/bin/python2
#Function not imported in the edgedetection project
import Image

def edgedrawer(threshold):
   image = Image.open('/home/victor/Pictures/copy.png')
   width, height = image.size
   newimage = Image.new('RGB', (width, height))
   for x in xrange(0, width):
      for y in xrange(0, height):
         nbh = neighborhood(x, y, width, height)
         g = []
         i=0
         for m in masks:
            g.append(0)
            j=0
            for n in m:
               w, h = nbh[j]
                      if w >= 0 and h >= 0 and w < width-1 and h < height-1:
                  value = image.getpixel(nbh[j])
                  gray = (value[0]+value[1]+value[2])/3
                  g[i] += gray*n
               j+=1
            i+=1
         mag = max(g)
         if mag > threshold:
            newimage.putpixel((x, y), (255, 255, 255))
         else:
            newimage.putpixel((x, y), (0, 0, 0))
   newimage.save('/home/victor/Pictures/newimage2.png')
