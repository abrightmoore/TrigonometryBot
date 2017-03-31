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

def popcornH(img,hconst): # http://paulbourke.net/fractals/popcorn/popcorn.c

	width = img.size[0]
	height = img.size[1]
	scale = 10 #random() * 20
	# hconst = 0.001 * randint(1,60)

	#scale = width
	N = 1000 #randint(400,1000)
	M = 0.1 #randint(5,20)

	max = 0
	pix = img.load()
	i = float(0)
	while i < width:
		j = float(0)
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
					(r,g,b,a) = pix[ix,iy]
					v = (r<<16)+(g<<8)+b
					v = v+1
					if v == 0:
						v = 128
					if v > max:
						max = v
					pix[ix,iy] = ((v&0xff0000)>>16,(v&0xff00)>>8,(v&0xff),255)
					# print pix[ix,iy]
				x = xnew
				y = ynew
			j = M+j
		i = M+i

def stubby():
	# Re-render image in colours
	print "Painting pixels..."
	coloursArray = [[(0.0,0,7,100),(0.16,32,107,203),(0.42,237,255,255),(0.6425,255,170,0),(0.8575,0,2,0),(1.0,30,0,0)], # after NightElfik
					[(0.0,0,randint(10,100),randint(10,100)),(0.16,randint(10,100),randint(10,107),randint(10,203)),(0.42,randint(10,235),randint(10,255),randint(10,255)),(0.6425,randint(10,255),randint(10,170),0),(0.8575,0,2,0),(1.0,30,0,0)],
					[(0.0,0,randint(128,255),randint(128,255)),(0.16,randint(128,255),randint(128,255),randint(128,256)),(0.42,randint(128,255),randint(128,255),randint(128,255)),(0.6425,randint(128,255),randint(128,255),0),(0.8575,0,2,0),(1.0,30,0,0)],
					
					]
	colours = coloursArray[0] #randint(0,len(coloursArray)-1)] 
	print "Max "+str(max)
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pix[x,y]
			count = (r<<16)+(g<<8)+b
			#remap to colour
			posn = float(count)/float(max)
			(p1, r1, g1, b1) = colours[0]
			for (p2, r2, g2, b2) in colours:
					if p1 <= posn and posn < p2:
							posnDelta = posn - p1
							gap = p2 - p1
							colPos = posnDelta/gap
							
							pix[x,y] = (int(r1+colPos*(r2-r1))%256,
												  int(g1+colPos*(g2-g1))%256,
												  int(b1+colPos*(b2-b1))%256,255)
							exit
					(p1, r1, g1, b1) = (p2, r2, g2, b2)			