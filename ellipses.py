#!/usr/bin/python2
import edgedetector
import shapesdetector
from imageprocessing import openImage
from sys import argv
import Image, ImageDraw
from cv_lab.colors import color
from random import choice
import pickle
from math import sin, cos
  

def detectellipses(image):
    pixels = image.load()
    width, height = image.size
    #magnitudes, angles = edgedetector.edgedetection(image)
    #nshapes, shapes = shapesdetector.getshapes(width, height, pixels)
    #pickle.dump(shapes, open('shapes.txt', 'w'))
    #pickle.dump(angles, open('angles.txt', 'w'))
    shapes = pickle.load(open('shapes.txt', 'r'))
    angles = pickle.load(open('angles.txt', 'r'))
    #print shapes
    nshapes = 4
    norandomps = 40
    draw = ImageDraw.Draw(image)
    for shape in shapes:
        if (0, 0) in shape:
            nshapes-=1
            shapes.remove(shape)
#        print nshapes
        for n in xrange(0, norandomps):
            # Two random points
            p1 = choice(shape)
            p2 = choice(shape)
            xp1, yp1 = p1[0], p1[1]
            xp2, yp2 = p2[0], p2[1]
            # Midpoint
            xm = (xp1+xp2)/2
            ym = (yp1+yp2)/2
#            draw.ellipse((xm-1, ym-1, xm+1, ym+1), fill='green')

            #print xp1, yp1, xp2, yp2
            thetap1 = angles[xp1][yp1]
            thetap2 = angles[xp2][yp2]
#            print thetap1, thetap2
            
            tsize = 50
            if thetap1 is not None and thetap2 is not None:
                # Tangent P1
                xap1 = xp1 - tsize*cos(thetap1)
                yap1 = yp1 - tsize*sin(thetap1)
                xbp1 = xp1 + tsize*cos(thetap1)
                ybp1 = yp1 + tsize*cos(thetap1)
                tangentP1 = (xap1, yap1, xbp1, ybp1)
                # Draw tangent P1
                #draw.line(tangentP1, fill='yellow')
                # Tangent P2
                xap2 = xp2 - tsize*cos(thetap2)
                yap2 = yp2 - tsize*sin(thetap2)
                xbp2 = xp2 + tsize*cos(thetap2)
                ybp2 = yp2 + tsize*cos(thetap2)
                tangentP2 = (xap2, yap2, xbp2, ybp2)
                # Draw tangent P2
                #draw.line(tangentP2, fill='yellow')
                
                # Intersection
                # From Wikipedia http://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
                
                
                try:
                    Denominador = (xap1-xbp1)*(yap2-ybp2)-(yap1-ybp1)*(xap2-xbp2)
                    PF1 = (xap1*ybp1-yap1*xbp1)
                    PF2 = (xap2*ybp2-yap2*xbp2)
                    Px = (PF1*(xap2-xbp2)-(xap1-xbp1)*PF2)/Denominador
                    Py = (PF1*(yap2-ybp2)-(yap1-ybp1)*PF2)/Denominador
                    draw.ellipse((Px-1, Py-1, Px+1, Py+1), fill='red')
                    # Line intersection - midpoint
                    draw.line((Px, Py, xm, ym), fill='white')
                except:
                    pass
                
                               

    print shapes
    image.save("tangents.png")        

if __name__=='__main__':
    try:
        image = Image.open(argv[1])
    except:
        image = openImage()
    detectellipses(image)
