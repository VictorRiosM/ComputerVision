#!/usr/bin/python2
import Tkinter, tkFileDialog
import Image, ImageDraw

def draw():
   image = Image.new('RGB', (100, 100))
   draw = ImageDraw.Draw(image)
   draw.ellipse((5, 5, 20, 30), fill='yellow')
   draw.ellipse((10, 35, 45, 45), fill='blue')
   draw.ellipse((37, 10, 45, 20), fill = 'green')
   name = raw_input("Name of the new image: ")
   image.save(name)
   
def openImage(file_path = None):
   if file_path == None:
      root = Tkinter.Tk()
      root.withdraw()
      file_path = tkFileDialog.askopenfilename()
      image = Image.open(file_path)
   else:
      image = Image.open(file_path)
   return image
      
def getbgcolor(image):
   w, h = image.size
   colors = {}
   for x in xrange(0, w):
      for y in xrange(0, h):
         c = image.getpixel((x, y))
         number = colors.get(c, None)
         if number == None:
            colors[c] = 1
         else:
            colors[c] = number + 1
   maximum = max(colors.values())
   print colors
   for c in colors:
      if colors[c] == maximum:
         bgcolor = c
   return bgcolor

def findFigure(image):
   w, h = image.size
   xmin = w
   xmax = 0
   ymin = h
   ymax = 0
   bgcolor = getbgcolor(image)
   for x in xrange(0, w):
      for y in xrange(0, h):
         if image.getpixel((x, y)) != bgcolor:
            if x < xmin:
               xmin = x
            if x > xmax:
               xmax = x
            if y < ymin:
               ymin = y
            if y > ymax:
               ymax = y
   draw = ImageDraw.Draw(image)
   draw.rectangle((xmin, ymin, xmax, ymax), outline = 'green')
   image.save('newimage.png')

def dfs(image):
   bgcolor = getbgcolor(image)
   w, h = image.size[0], image.size[1]
   print w, h
   start = 0, 0
   s = list()
   s.append(start)
   visited = list()
   figures = list()
   while len(s)!=0:
      x, y = s.pop()
      if (x, y) not in visited:
         if x < w and y < h and x >= 0 and y >= 0:
            if image.getpixel((x, y)) != bgcolor:
               figures.append((x, y))
            visited.append((x, y))
            s.extend(neighborhood(x, y))
   return figures

def neighborhood(x, y):
   nbh = list()
   nbh.append((x-1, y-1))
   nbh.append((x, y-1))
   nbh.append((x+1, y-1))
   nbh.append((x-1, y))
   nbh.append((x, y))
   nbh.append((x+1, y))
   nbh.append((x-1, y+1))
   nbh.append((x, y+1))
   nbh.append((x+1, y+1))
   return nbh

  
def main():
   draw()
   #image = Image.open('image.png')
   #findFigure(image)

if __name__=='__main__':
   main()
