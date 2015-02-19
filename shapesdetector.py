#!/usr/bin/python2
import Image
from sys import argv
from imageprocessing import openImage
from imageprocessing import neighborhood

def detectshapes(image):
   pixels = image.load()
   width, height = image.size
   visited = []
   nshapes = 0
   i=0
   for x in xrange(0, width):
      for y in xrange(0, height):
         #print pixels[x, y]
         if pixels[x, y] != (0, 0, 0):
            i+=1
         if (x, y) not in visited and pixels[x, y] != (0, 0, 0):
            nshapes += 1
            print "nshapes", nshapes
            #DFS
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
            visited.extend(s_visited)
         visited.append((x, y))
   print i
   print len(visited)
   print width, height, width*height, nshapes

if __name__=='__main__':
   try:
      image = Image.open(argv[1])
   except:
      image = openImage()
   detectshapes(image)
