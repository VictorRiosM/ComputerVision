#!/usr/bin/python2
import Image
from sys import argv
from imageprocessing import neighborhood
from imageprocessing import openImage

# These are the masks I use in order to detect edges
A=1
B=-1
masks = [ [B, 0, A, B, 0, A, B, 0, A],
          [0, A, A, B, 0, A, B, B, 0],
          [A, A, A, 0, 0, 0, B, B, B],
          [A, A, 0, A, 0, B, 0, B, B],
          [A, 0, B, A, 0, B, A, 0, B],
          [0, B, B, A, 0, B, A, A, 0],
          [B, B, B, 0, 0, 0, A, A, A],
          [B, B, 0, B, 0, A, 0, A, A] ]

         
#The subroutine that computes the magnitudes and draws an image remarking the edges.
def edgedetection(image, threshold = None):
   width, height = image.size
   if threshold == None:
      magnitudes = {}
   else:
      newimage = Image.new('RGB', (width, height))
   for x in xrange(0, width):
      for y in xrange(0, height):
         nbh = neighborhood(x, y)
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
         if threshold == None:
            frequency = magnitudes.get(mag, None)
            if frequency == None:
               magnitudes[mag] = 1
            else:
               magnitudes[mag] = frequency + 1
         elif mag > threshold:
            newimage.putpixel((x, y), (255, 255, 255))
         else:
            newimage.putpixel((x, y), (0, 0, 0))
   if threshold == None:
      return magnitudes
   else:
      newimage.save('newimage.png')


def delimitthreshold(magnitudes):
   j=20
   discrete={}
   lastkey=magnitudes.keys()[-1]

   for i in xrange(0, lastkey+1):
      if magnitudes.has_key(i):
         f = discrete.get(j, None)
         if f == None:
            discrete[j] = magnitudes[i]
         else:
            discrete[j] = f+magnitudes[i]
      if i%20 == 0 and i > 0:
         j += 20

   print discrete.viewitems()
   

   minimum = max(discrete.values())
   for key in discrete:
      if discrete[key] == minimum:
         threshold = key
   print threshold
   return threshold


def main():
   try:
      image = Image.open(argv[1])
   except:
      image = openImage()
   #Calling edgedetection with an image as argument returns a histogram with the frequencies
   magnitudes = edgedetection(image)
#   print magnitudes
   threshold = delimitthreshold(magnitudes)
   #edgedetection draws a new image if threshold is given
   edgedetection(image, threshold)

if __name__=='__main__':
   main()
   
