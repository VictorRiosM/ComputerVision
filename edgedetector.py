#!/usr/bin/python2
import Image
from sys import argv
from imageprocessing import neighborhood
from imageprocessing import openImage
from math import atan2, pi

# These are the masks I use in order to detect edges
#A=1
#B=-1
#masks = [ [B, 0, A, B, 0, A, B, 0, A], # 0
#          [0, A, A, B, 0, A, B, B, 0], # 45
#          [A, A, A, 0, 0, 0, B, B, B], # 90
#          [A, A, 0, A, 0, B, 0, B, B], # 135
#          [A, 0, B, A, 0, B, A, 0, B], # 180
#          [0, B, B, A, 0, B, A, A, 0], # 225
#          [B, B, B, 0, 0, 0, A, A, A], # 270
#          [B, B, 0, B, 0, A, 0, A, A] ] # 315

masks = [ [-1, 0, 1, -2, 0, 2, -1, 0, 1],
          [1, 2, 1, 0, 0, 0, -1, -2, -1] ]


# Convolution
def convolution(pixels, width, height):
   magnitudes = []
   angles = []
   for y in xrange(0, height):
      gcols = []
      acols = []
      for x in xrange(0, width):
         gx = 0
         gy = 0
         index = 0
         for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
               if x+i >= 0 and x+i < width and y+j >= 0 and y+j < height:
                  rgb = pixels[x+i, y+j]
                  gray = (rgb[0] + rgb[1] + rgb[2]) / 3
                  gx += gray*masks[0][index]
                  gy += gray*masks[1][index]
                  index += 1
         g = max(abs(gx), abs(gy))
         theta = atan2(gy, gx)
         gcols.append(g)
         acols.append(theta)
      magnitudes.append(gcols)
      angles.append(acols)
   return magnitudes, angles


def drawedges(pixels, magnitudes, width, height, threshold):
   for y in xrange(0, height-1):
      for x in xrange(0, width-1):
         if magnitudes[y][x] > threshold:
            pixels[x, y] = (255, 255, 255)
         else:
            pixels[x, y] = (0, 0, 0)
   return pixels


def edgedetect(image):
   pixels = image.load()
   width, height = image.size
   magnitudes, angles = convolution(pixels, width, height)
   threshold = 100
   pixels = drawedges(pixels, magnitudes, width, height, threshold)
   image.save("edge.png")
   image.show()
         
#The subroutine that computes the magnitudes and draws an image remarking the edges.
def edgedetection(image, threshold = None):
   width, height = image.size
   pixels = image.load()
   angles = []
   if threshold == None:
      magnitudes = {}
   else:
      newimage = Image.new('RGB', (width, height))
   for x in xrange(0, width):
      pixelsorientation = []
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

         # Magnitude
         mag = max(abs(g[0]), abs(g[1]))
         #mag = max(g) # Select the maximum gradient: the magnitud

         # Angles
         orientation=atan2(g[1], g[0])
         if orientation < 0:
            orientation += pi*2
         #orientation = (orientation - pi/2)
         #orientation=abs(orientation-pi/2)
         #if orientation < 0.0001:
         #   orientation = None
         pixelsorientation.append(orientation)        
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
      angles.append(pixelsorientation)
   if threshold == None:
      return magnitudes, angles
      
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
   #magnitudes, pixelsorientation = edgedetection(image)
   #hist, bins = np.histogram(magnitudes.values(), bins=10)
   #width = 0.7 * (bins[1]-bins[0])
   #center = (bins[:-1] + bins[1:])/2
   #threshold = delimitthreshold(magnitudes)
   #edgedetection draws a new image if threshold is given
   #edgedetection(image, threshold)
   edgedetect(image)

if __name__=='__main__':
   main()
   
