# @abrightmoore
# from numpy import *
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys

from PIL import Image, ImageDraw

from ImageTools import *


def draw(img_orig):
	imgArray = []
	ox,oy,sx,sy = (-2.0,-1.5,3.0,3.0)
	img = Image.new('RGBA', size=(100,100), color=(0, 0, 0, 255))
	(new_ox,new_oy,new_sx,new_sy) = drawMandelbrot(img,ox,oy,sx,sy)
	for i in xrange(0,5): # This section finds a deep layer in the Mandelbrot
		(new_ox,new_oy,new_sx,new_sy) = drawMandelbrot(img,ox,oy,sx,sy)
		ox = new_ox
		oy = new_oy
		sx = new_sx
		sy = new_sy
		imgArray.append(img)
	img = Image.new('RGBA', size=img_orig.size, color=(0, 0, 0, 255))
	drawMandelbrot(img,ox,oy,sx,sy)
	#imageBlend(img_orig,imgArray[len(imgArray)-1])
	imageBlend(img_orig,img)

def drawMandelbrot(img,ox,oy,sx,sy):
	width = img.size[0]
	height = img.size[1]
	img.paste( (0,0,0), [0,0,width,height])
        MAXITER = 256
        coloursArray = [[(0.0,0,7,100),(0.16,32,107,203),(0.42,237,255,255),(0.6425,255,170,0),(0.8575,0,2,0),(1.0,30,0,0)], # after NightElfik
                        [(0.0,0,randint(10,100),randint(10,100)),(0.16,randint(10,100),randint(10,107),randint(10,203)),(0.42,randint(10,235),randint(10,255),randint(10,255)),(0.6425,randint(10,255),randint(10,170),0),(0.8575,0,2,0),(1.0,30,0,0)],
						[(0.0,0,randint(128,255),randint(128,255)),(0.16,randint(128,255),randint(128,255),randint(128,256)),(0.42,randint(128,255),randint(128,255),randint(128,255)),(0.6425,randint(128,255),randint(128,255),0),(0.8575,0,2,0),(1.0,30,0,0)],
						
                        ]
        colours = coloursArray[randint(0,len(coloursArray)-1)]              
        # Window on the number plane

        qx = sx/float(width) # Quantum of distance
        qy = sy/float(height) # Quantum of distance

        nextP = (-1.0,0.0)
        pixels = img.load()
        for x in xrange(0,width):
                for y in xrange(0,height):
                        px = ox+qx*x # real 
                        py = oy+qy*y # imaginary
                        # print px,py
                        count = MAXITER
                        dist2 = px**2+py**2
                        cx = px
                        cy = py
                        while count >=0 and dist2 < 4:
                                count = count-1
                                x_new = cx**2 - cy**2 + px
                                cy = 2*cx*cy + py
                                cx = x_new
                                dist2 = cx**2 + cy**2
                        if count > 0:
                                posn = float(count)/float(MAXITER)
                                (p1, r1, g1, b1) = colours[0]
                                for (p2, r2, g2, b2) in colours:
                                        if p1 <= posn and posn < p2:
                                                posnDelta = posn - p1
                                                gap = p2 - p1
                                                colPos = posnDelta/gap
                                                
                                                pixels[x,y] = (int(r1+colPos*(r2-r1))%256,
                                                                      int(g1+colPos*(g2-g1))%256,
                                                                      int(b1+colPos*(b2-b1))%256,255)
#                                               if count < 10 and random() < 0.5: # and count < MAXITER-MAXITER>>2: choose a zoom
#                                                        nextP = (px,py)
#                                                        print nextP
                                                exit
                                        (p1, r1, g1, b1) = (p2, r2, g2, b2)

                        else:
                                pixels[x,y] = (0,0,80,255)
        # Work out where to go next
        diffImg = imageAvgDiff(img)
        zoomCol = (255,255,0,255)
        zoomRadius = randint(10,width>>2)
        pixDiff = diffImg.load()
        P = []
        for x in xrange(0,width-2):
                for y in xrange(0,height-2):
                        (r,g,b,a) = pixDiff[x,y]
                        if r > 32 and random() < 0.01: # Threshhold for finding interesting edges
                                pixDiff[x,y] = (255,0,0,255)
                                P.append((x,y))
        # diffImg.save("Diff"+str(randint(111111111,999999999))+".png")
        if len(P) > 0:
                (x,y) = P[randint(0,len(P)-1)]
                px = ox+qx*x
                py = oy+qy*y
                for ix in xrange(x-zoomRadius,x+zoomRadius):
                        if ix >0 and ix < width-1:
                                if y-zoomRadius > 0:
                                        pixDiff[ix-1,y-zoomRadius-1] = zoomCol                                              
                                if y+zoomRadius < height-1:
                                        pixDiff[ix-1,y+zoomRadius-1] = zoomCol
                for iy in xrange(y-zoomRadius,y+zoomRadius):
                        if iy >0 and iy < height-1:
                                if x-zoomRadius > 0:
                                        pixDiff[x-zoomRadius-1,iy-1] = zoomCol                                              
                                if x+zoomRadius < width-1:
                                        pixDiff[x+zoomRadius-1,iy-1] = zoomCol
                                                
                #diffImg.save("Diff"+str(randint(111111111,999999999))+".png")
                return (px-zoomRadius*qx,py-zoomRadius*qx,zoomRadius*2*qx,zoomRadius*2*qy)
        else:
                return (-2.0,-1.5,3.0,3.0) # Top level again, couldn't find a point to play with
