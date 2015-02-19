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

    

# import matplotlib.pyplot as plt
# import matplotlib.cm as cmx
# import matplotlib.colors as colors

# def get_cmap(N):
#     '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
#     RGB color.'''
#     color_norm  = colors.Normalize(vmin=0, vmax=N-1)
#     scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
#     def map_index_to_rgb_color(index):
#         return scalar_map.to_rgba(index)
#     return map_index_to_rgb_color

# def main():
#     N = 5
#     fig=plt.figure()
#     ax=fig.add_subplot(111)   
#     plt.axis('scaled')
#     ax.set_xlim([ 0, N])
#     ax.set_ylim([-0.5, 0.5])
#     cmap = get_cmap(N)
#     for i in range(N):
#         col = cmap(i)
#         rect = plt.Rectangle((i, -0.5), 1, 1, facecolor=col)
#         ax.add_artist(rect)
#     ax.set_yticks([])
#     plt.show()

# if __name__=='__main__':
#     main()
