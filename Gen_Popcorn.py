# @abrightmoore
# from numpy import *
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys
from numpy import *

from PIL import Image, ImageDraw

from ImageTools import *
from Gen_Trigonometry import calcFormula
from Colours import *

def draw(img):
	chance = random()
	if chance < 0.3:
		popcorn1(img)
	elif chance < 1.0:
		popcorn2(img)
	else:
		popcorn3(img) # With colour - under test

def popcorn3(img): # http://paulbourke.net/fractals/popcorn/popcorn.c

	width = img.size[0]
	height = img.size[1]
	img2 = Image.new("RGBA",size=(width,height),color=(0,0,0))
	scale = 1000 #random() * 20+0.01
	hconst = 0.5 #0.01 * randint(1,5)

	#scale = width
	N = 1000
	M = 0.1 #randint(5,20)
		
	C = getColoursBrownian(randint(32,128),randint(4,16))		
#	C = getRandomAnalogousColours()		
	print C
	pix = img2.load()
	i = 0
	while i < width:
		j = 0
		while j < height:
			x = float(2.0 * scale * (float(i) - float(width) / 2.0) / float(width))
			y = float(2.0 * scale * (float(j) - float(height) / 2.0) / float(height))
			for n in xrange(0,N):
				xnew = float(x - hconst * sin(y + tan(3 * y)))
				ynew = float(y - hconst * sin(x + tan(3 * x)))
				ix = 0.5 * xnew * float(width) / scale + float(width) / 2.0;
				iy = 0.5 * ynew * float(height) / scale + float(height) / 2.0; 
				if (ix >= 0 and iy >= 0 and ix < width and iy < height):
					(vr,vg,vb) = pix[ix,iy]
					colour = ((vr+1)%255,(vg+1)%255,(vb+1)%255,255)
					pix[ix,iy] = colour
				x = xnew
				y = ynew
			j = j+M
		i = i +M

	px = img.load()
	max = 0
	min = 255
	for x in xrange(0,width):
		for y in xrange(0,height):
			(vr,vg,vb) = pix[x,y]
			(r,g,b) = C[vr%len(C)]
			px[x,y] = (r,g,b,255)
			if vr > max:
				max = vr
			if vr < min:
				min = vr
	print min,max
	img2.save("imagesTest\\testonly_"+str(randint(1000000,9999999))+".png")
		

def popcorn2(img): # http://paulbourke.net/fractals/popcorn/popcorn.c
	width = img.size[0]
	height = img.size[1]
	scale = random() * 20
	hconst = 0.001 * randint(1,60)

	#scale = width
	N = randint(400,1000)
	M = randint(5,20)

	pix = img.load()
	i = 0
	while i < width:
		j = 0
		while j < height:
			x = float(2.0 * scale * (i - width / 2) / width)
			y = float(2.0 * scale * (j - height / 2) / height)
			for n in xrange(0,N):
				xnew = float(x - hconst * sin(y + tan(3 * y)))
				ynew = float(y - hconst * sin(x + tan(3 * x)))
				ix = 0.5 * xnew * width / scale + width / 2;
				iy = 0.5 * ynew * height / scale + height / 2; 
				if (ix >= 0 and iy >= 0 and ix < width and iy < height):
					(vr,vg,vb,va) = pix[ix,iy]
					colour = ((vr+16)%255,(vg+16)%255,(vb+16)%255,va)
					pix[ix,iy] = colour
				x = xnew
				y = ynew
			j = j+M
		i = i +M
	
def popcorn1(img): # http://paulbourke.net/fractals/popcorn/popcorn.c
	width = img.size[0]
	height = img.size[1]
	scale = random() * 20
	hconst = 0.001 * randint(1,60)

	#scale = width
	N = randint(400,1000)
	M = randint(5,20)

	pix = img.load()
	i = 0
	while i < width:
		j = 0
		while j < height:
			x = float(2.0 * scale * (i - width / 2) / width)
			y = float(2.0 * scale * (j - height / 2) / height)
			for n in xrange(0,N):
				xnew = float(x - hconst * sin(y + tan(3 * y)))
				ynew = float(y - hconst * sin(x + tan(3 * x)))
				colour = (n/N*255,n/N*255,n/N*255,255)
				ix = 0.5 * xnew * width / scale + width / 2;
				iy = 0.5 * ynew * height / scale + height / 2; 
				if (ix >= 0 and iy >= 0 and ix < width and iy < height):
					pix[ix,iy] = colour
				x = xnew
				y = ynew
			j = j+M
		i = i +M
