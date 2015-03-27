#!/usr/bin/python2
import Image
from imageprocessing import openImage
from sys import argv

def resize(image, enorshrink, mode):
   pixels = image.load()
   width, height = image.size
   
   # Enlarge
   if enorshrink=='e':
      if mode=='p':
         factor = input('Factor: ')
         newimage = Image.new('RGB', (width*factor, height*factor))
         i=0
         for x in xrange(0, width*factor):
            j=0
            for y in xrange(0, height*factor):
               newimage.putpixel((x, y), pixels[i, j])
               if y%factor+1==factor:
                  j+=1
            if x%factor+1==factor:
               i+=1
         newimage.save('enlarged.png')
         newimage.show()

   # Shrink
#   elif enorshrink=='s':

   

if __name__=='__main__':
   try:
      image=Image.open(argv[1])
   except:
      image=openImage()
   try:
      enorshrink=argv[2] 
   except:
      enorshrink=raw_input("Enlarge[e], shrink[s]: ")
   try:
      mode=argv[3]
   except:
      mode=raw_input("Proportional[p], Arbitrary[a]: ")
   resize(image, enorshrink, mode)
