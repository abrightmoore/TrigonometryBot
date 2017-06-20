# @abrightmoore

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2

from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
import sys
from io import BytesIO
from numpy import *
from random import randint, random, Random

from PIL import Image, ImageDraw

from CircleStack import CircleStack
from ImageTools import *

#import Palette # @abrightmoore

def draw(img):
	width = img.size[0]
	height = img.size[1]	
	centre = (width>>1,height>>1)
	imgA = Image.new('RGBA', size=(width, height), color=(0,0,0, 255))
	
	RADIUS = randint(width>>5,width>>3)
	
	cols = int(width/(RADIUS<<1))
	rows = int(height/(RADIUS<<1))	
	#print rows,cols
	hgap = (width-cols*(RADIUS<<1))>>1
	vgap = (height-rows*(RADIUS<<1))>>1
	print hgap,vgap
	
	matrix = zeros((cols,rows))
	CIRCLES = []
	for i in xrange(0,cols):
		for j in xrange(0,rows):
			pos = (0,0)
			if random() > 0.5 and i < cols-1 and j < rows-1 and matrix[i,j] == 0 and matrix[i+1,j] == 0 and matrix[i,j+1] == 0 and matrix[i+1,j+1] == 0:
				matrix[i,j] = 1
				matrix[i+1,j] = 1
				matrix[i,j+1] = 1
				matrix[i+1,j+1] = 1
				pos = ((i+1)*(RADIUS<<1)+hgap,(j+1)*(RADIUS<<1)+vgap)
				circle = CircleStack(pos,RADIUS<<1,randint(8,32))

			elif matrix[i,j] == 0:
				pos = (i*(RADIUS<<1)+RADIUS+hgap,j*(RADIUS<<1)+RADIUS+vgap)
				matrix[i,j] = 1
				circle = CircleStack(pos,RADIUS,randint(4,12))
			if pos != (0,0):
				CIRCLES.append(circle)
		
	loc = (randint(0,width),randint(0,height))
	randomness = 0.1*randint(0,9)
	for circle in CIRCLES:
		if random() > randomness:
			loc = (randint(0,width),randint(0,height))
		circle.draw(imgA,loc)
#	filename =  "O_"+str(randint(1000000000,9999999999))
#	imgA.save(filename+"_normalized.png")
	mergeImagesInPlace(img,imgA)
#	filename =  "O_m_"+str(randint(1000000000,9999999999))
#	img.save(filename+"_normalized.png")
	
def mergeImagesInPlace(img1,img2):
	# Assumes both images are the same dimensions
	width = img1.size[0]
	height = img1.size[1]
	width2 = img2.size[0]
	height2 = img2.size[1]
	if width2 != width or height2 != height:
		img2 = img2.resize((width,height), Image.ANTIALIAS)
		width2 = img2.size[0]
		height2 = img2.size[1]

	gapx = (width-width2)>>1
	gapy = (height-height2)>>1
	pix = img1.load()
	pix2 = img2.load()

	for x in xrange(0,width):
		for y in xrange(0,height):
			(r1,g1,b1,a1) = pix[x,y]
			(r2,g2,b2,a2) = pix2[x,y]
			ratio = 0.5
			ratioInv = 1.0-ratio
			(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
			if r > 255:
				r = 255
			if g > 255:
				g = 255
			if b > 255:
				b = 255
			pix[x,y] = (int(r),int(g),int(b),int(a))
