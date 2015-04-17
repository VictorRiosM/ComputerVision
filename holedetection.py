#!/usr/bin/python2
import Image, ImageDraw
from imageprocessing import openImage
from sys import argv
from cv_laboratorio.filter import filter

def colorshistogram(pixels, width, height):
    histo = dict()
    for x in xrange(0, width):
       for y in xrange(0, height):
            if pixels[x, y] in histo:
                histo[pixels[x, y]] += 1
            else:
                histo[pixels[x, y]] = 1
    return histo
    

def paintbg(pixels, width, height, bgcolor, ncolor):
    for x in xrange(0, width):
        for y in xrange(0, height):
            (r, g, b) = pixels[x, y]
            (bgr, bgg, bgb) = bgcolor
            bgthresh = 40
            if r > bgr-bgthresh and r < bgr+bgthresh and g > bgg-bgthresh and g < bgg+bgthresh and b > bgb-bgthresh and b < bgb+bgthresh:
                pixels[x, y] = ncolor
            else:
                (r, g, b) = pixels[x, y]
                gray = int((r+g+b)/3)
                r = g = b = gray
                pixels[x, y] = (r, g, b)
    return pixels


def rows_cols_histograms(pixels, width, height):
    rows_histo = dict()
    cols_histo = dict()
    for x in xrange(0, width):
        cols_histo[x] = 0
        for y in xrange(0, height):
            (r, g, b) = pixels[x, y]
            gray = int((r+g+b)/3)
            cols_histo[x] += gray
            if y in rows_histo:
                rows_histo[y] += gray
            else:
                rows_histo[y] = gray
            if x == width-1:
                rows_histo[y] = int(rows_histo[y]/width)
        cols_histo[x] = int(cols_histo[x]/height)
    return rows_histo, cols_histo


def drawpikes(image, rows_histo, cols_histo, rows_threshold, cols_threshold):
    pix = image.load()
    width, height = image.size
    draw = ImageDraw.Draw(image)
    x_prob=[]
    y_prob=[]
    for x in xrange(0, width):
        if cols_histo[x] < cols_threshold:
            draw.line((x, 0, x, height-1), fill='red')
            x_prob.append(x)
    for y in xrange(0, height):
        if rows_histo[y] < rows_threshold:
            draw.line((0, y, width-1, y), fill='blue')
            y_prob.append(y)
    image.save("pikes.png")
    return x_prob, y_prob            


def getholes(image, x_prob, y_prob):
    width, height = image.size
    pixels = image.load()
    visited = list()
    hole_pixels = list()
    for x in xrange(0, width):
        for y in xrange(0, height):
            if x in x_prob and y in y_prob and pixels[x, y] != (255, 255, 255):
                hole_pixels.append((x, y))
    return hole_pixels
    


def holedetection(image):
    pixels = image.load()
    holes_in_original = image.copy()
    width, height = image.size
    colorshisto = colorshistogram(pixels, width, height)
    maxcolor = max(colorshisto.values())
    print maxcolor
    for key in colorshisto:
        if colorshisto[key] == maxcolor:
            bgcolor = key
            break
    print bgcolor
    #pixels = filter(image)
    pixels = paintbg(pixels, width, height, bgcolor, (255, 255, 255))
    #pixels = filter(image)
    image.save('gray.png')
    holes_image = image.copy()
    rows_histo, cols_histo = rows_cols_histograms(pixels, width, height)
    #print rows_histo, cols_histo
    
    rows_threshold = int(sum(rows_histo.values())/height)
    cols_threshold = int(sum(cols_histo.values())/width)
    #rows_threshold = max(rows_histo.values())
    #cols_threshold = max(cols_histo.values())
    print rows_threshold
    print cols_threshold
    
    x_prob, y_prob = drawpikes(image, rows_histo, cols_histo, rows_threshold, cols_threshold)
    #print rows_median, cols_median
    #image.save("pikes.png")
    print x_prob, y_prob
    hole_pixels=getholes(holes_image, x_prob, y_prob)
    
    pixels2 = holes_in_original.load()
    for pixel in hole_pixels:
        pixels2[pixel] = (0, 255, 0)
    holes_in_original.save('hole_pixels.png')


if __name__=='__main__':
    try:
        image = Image.open(argv[1]).convert("RGB")
    except:
        image = openImage().convert("RGB")
    holedetection(image)
