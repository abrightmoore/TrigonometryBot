from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint, random, Random
from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
import pygame, sys
from pygame.locals import *
from io import BytesIO
import imageio
from numpy import *

from Colours import *
from ImageTools import *
			
			
def interpolateCol(colours,posn):
	result = (0,0,0)
	(p1, r1, g1, b1) = colours[0]
	for (p2, r2, g2, b2) in colours:
		if p1 <= posn and posn < p2:
			posnDelta = posn - p1
			gap = p2 - p1
			colPos = float(posnDelta)/gap			
			result = (int(r1+colPos*(r2-r1))%256,
				  int(g1+colPos*(g2-g1))%256,
				  int(b1+colPos*(b2-b1))%256)
		(p1, r1, g1, b1) = (p2, r2, g2, b2)
	return result
	
def draw(img):
	width = img.size[0]
	height = img.size[1]	
	COLS_BOOM = [
			(0.0,70,60,20),
			(0.10,128,0,20),
			(0.3,240,56,40),
			(0.7,240,240,0),
			(0.9,0,100,255),
			(1.0,255,255,255)
		]
	COLS_RAND = [
			(0.0,randint(0,255),randint(0,255),randint(0,255)),
			(0.10,randint(0,255),randint(0,255),randint(0,255)),
			(0.3,randint(0,255),randint(0,255),randint(0,255)),
			(0.7,randint(0,255),randint(0,255),randint(0,255)),
			(0.9,randint(0,255),randint(0,255),randint(0,255)),
			(1.0,randint(0,255),randint(0,255),randint(0,255))
		]

	COLS = COLS_BOOM
	if random() > 0.5:
		COLS = COLS_RAND
		
	pixels = img.load()

	angle = pi/height
	for y in xrange(0,height):
		for x in xrange(0,width):
			(r,g,b,a) = pixels[x,y]
			(r1,g1,b1) = interpolateCol(COLS,cos(float(x)/float(width)*angle*y))
			pixels[x,y] = ((r+r1)>>1,(g+g1)>>1,(b+b1)>>1,a)			

						
