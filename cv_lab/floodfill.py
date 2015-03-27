import Image

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
