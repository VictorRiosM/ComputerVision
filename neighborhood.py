#!/usr/bin/python2

def neighborhood(x, y, width, height):
   nbh = list()
   if x > 0 and y > 0 and x < width-1 and y < height-1:
      nbh.append((x-1, y-1))
      nbh.append((x, y-1))
      nbh.append((x+1, y-1))
      nbh.append((x-1, y))
      nbh.append((x, y))
      nbh.append((x+1, y))
      nbh.append((x-1, y+1))
      nbh.append((x, y+1))
      nbh.append((x+1, y+1))
   elif y > 0 and x < width-1 and y < height-1:
      nbh.append((x, y-1))
      nbh.append((x+1, y-1))
      nbh.append((x+1, y))
      nbh.append((x, y+1))
      nbh.append((x+1, y+1))
   elif x > 0 and x < width-1 and y < height-1:
      nbh.append((x-1, y))
      nbh.append((x+1, y))
      nbh.append((x-1, y+1))
      nbh.append((x, y+1))
      nbh.append((x+1, y+1))
   elif x > 0 and y > 0 and y < height:
      nbh.append((x-1, y-1))
      nbh.append((x, y-1))
      nbh.append((x-1, y))
      nbh.append((x-1, y+1))
      nbh.append((x, y+1))
   elif x > 0 and y > 0 and x < height:
      nbh.append((x-1, y-1))
      nbh.append((x, y-1))
      nbh.append((x+1, y-1))
      nbh.append((x-1, y))
      nbh.append((x+1, y))
   elif x == 0 and y == 0:
      nbh.append((x+1, y))
      nbh.append((x, y+1))
      nbh.append((x+1, y+1))
   elif x == width-1 and y == 0:
      nbh.append((x-1, y))
      nbh.append((x-1, y+1))
      nbh.append((x, y+1))
   elif x == 0 and y == height-1:
      nbh.append((x, y-1))
      nbh.append((x+1, y-1))
      nbh.append((x+1, y))
   elif x == width-1 and y == height-1:
      nbh.append((x-1, y-1))
      nbh.append((x, y-1))
      nbh.append((x-1, y))
   return nbh
