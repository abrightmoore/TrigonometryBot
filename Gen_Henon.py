# @abrightmoore
# After Paul Bourke, et. al.
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys
from numpy import *

from PIL import Image, ImageDraw
import imageio

from ImageTools import *
from Gen_Trigonometry import calcFormula
from Colours import *

def draw(img):

	henon(img)
	
def henon(img):
	width = img.size[0]
	height = img.size[1]
	angle = random()*pi*2.0
	ca = cos(angle)
	sa = sin(angle)
	r = 0.0
	p0x = 0.0
	p0y = 0.0
	p1x = 0.0
	p1y = 0.0
	nnew = 0
	
	MAXSTEPS = 1000000
	NX = width
	NY = height
	SCALE = NX/3
	
	C = getColoursBrownian(randint(16,64),randint(4,16))
	pix = img.load()
	col = 0
	#(rc,gc,bc) = (randint(0,255),randint(0,255),randint(0,255))
	for n in xrange(0,MAXSTEPS):
		r = p0x*p0x +p0y*p0y
		if r > 0xffff or n%(MAXSTEPS/1000) == 0:
			p0x = 2*random()-1
			p0y = 2*random()-1
			nnew = 0
		p1x = p0x * ca - (p0y - p0x*p0x) * sa
		p1y = p0x * sa + (p0y - p0x*p0x) * ca
		if nnew > 10:
			ix = p1x * SCALE + NX/2
			iy = p1y * SCALE + NY/2
			#colour = (rc,gc,bc,255)
			# print colour,ix,iy
			if ix >= 0 and iy >= 0 and ix < width and iy < height:
				pix[ix,iy] = C[col%len(C)]
		if random() < 0.001:
			col = col+1
		p0x = p1x
		p0y = p1y
		nnew = nnew+1