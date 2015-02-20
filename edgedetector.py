#!/usr/bin/python2
import Image
from sys import argv
from imageprocessing import neighborhood
from imageprocessing import openImage
import matplotlib.pyplot as plt
import numpy as np
import cv2

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
   pixels = image.load()
   if threshold == None:
      magnitudes = {}
   else:
      newimage = Image.new('RGB', (width, height))
   for x in xrange(0, width):
      for y in xrange(0, height):
         nbh = neighborhood(x, y) #Gets the pixel neighborhood
         g = [] # A list for the gradients
         i=0
         #Convolution
         for m in masks:
            g.append(0)
            j=0
            for n in m:
               w, h = nbh[j]
               if w >= 0 and h >= 0 and w < width and h < height:
                  #Gets a value from RGB
                  #value = image.getpixel(nbh[j])
                  value = pixels[nbh[j]]
                  gray = (value[0]+value[1]+value[2])/3
                  g[i] += gray*n 
               j+=1
            i+=1
         mag = max(g) #Select the maximum gradient: the magnitud
         if threshold == None:
            # Getting frequencies
            frequency = magnitudes.get(mag, None)
            if frequency == None:
               magnitudes[mag] = 1
            else:
               magnitudes[mag] = frequency + 1
         elif mag > threshold:
            # Puts white the pixels that exceeds the threshold
            newimage.putpixel((x, y), (255, 255, 255))
         else:
            # Puts black the pixels that don't exceeds the threshold
            newimage.putpixel((x, y), (0, 0, 0))
   if threshold == None:
      return magnitudes
   else:
      newimage.save('newimage.png')

# Thresholding
def delimitthreshold(magnitudes):
   j=20
   discrete={}
   lastkey=magnitudes.keys()[-1]
   # Makes buckets from the histogram of magnitudes
   for i in xrange(0, lastkey+1):
      if magnitudes.has_key(i):
         f = discrete.get(j, None)
         if f == None:
            discrete[j] = magnitudes[i]
         else:
            discrete[j] = f+magnitudes[i]
      if i%20 == 0 and i > 0:
         j += 20
   # Determining the threshold
   total = sum(discrete.values())
   half = total/2
   suma=0
   # While the sum of frequencies is not greater than the half
   threshold=0
   for key in discrete:
      threshold+=20
      suma += discrete[key]
      if suma > half:
         break
   return threshold

def main():
   try:
      image = Image.open(argv[1])
      #image = cv2.imread(argv[1])
   except:
      image = openImage()
   #Calling edgedetection with an image as argument returns a histogram with the frequencies
   magnitudes = edgedetection(image)
   hist, bins = np.histogram(magnitudes.values(), bins=10)
   width = 0.7 * (bins[1]-bins[0])
   center = (bins[:-1] + bins[1:])/2
#   plt.bar(center, hist, align='center', width=width)
#   plt.show()
   threshold = delimitthreshold(magnitudes)
   #edgedetection draws a new image if threshold is given
   edgedetection(image, threshold)

if __name__=='__main__':
   main()
   
