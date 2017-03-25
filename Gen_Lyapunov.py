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
	createAttractor(img)

def incVal(v,d,max):
	v = v+d
	if v> max:
		v = max
	return v

def saveAttractor(img,n,a,b,xmin,xmax,ymin,ymax,x,y): # https://gist.github.com/mrbichel/1871929
	width = img.size[0]
	height = img.size[1]
	img2 = Image.new("RGBA",size=(width,height),color=(148,148,148))
	
	MAXITERATIONS = 10000000
	#draw = ImageDraw.Draw(img2)
	pix = img2.load()
	px = img.load()
	for i in range(MAXITERATIONS):
		ix = width * (x[i] - xmin) / (xmax - xmin)
		iy = height * (y[i] - ymin) / (ymax - ymin)
		if i > 100:
			#draw.point([ix, iy], fill="black")
			if ix >= 0 and ix < width and iy >= 0 and iy < height:
				(r,g,b,a) = pix[ix,iy]
				pix[ix,iy] = (incVal(r,1,255),incVal(g,1,255),incVal(b,1,255),a)
				(r,g,b,a) = px[ix,iy]
				px[ix,iy] = (incVal(r,1,255),incVal(g,1,255),incVal(b,1,255),a)
	imageNormalize(img2)
	img2.save("imagesTest\\Lyapunov_"+str(n)+"_"+str(a)+"_"+str(b)+"_"+str(randint(1000000,9999999))+".png")
	C = getColoursBrownian(128,4)

	img3 = Image.new("RGBA",size=(width,height),color=(0,0,0))
	px3 = img3.load()
	for ix in xrange(0,width):
		for iy in xrange(0,height):
			(cr,cg,cb,a) = pix[ix,iy]
			px3[ix,iy] = C[cr%len(C)]
	imageNormalize(img3)
	img3.save("imagesTest\\Lyapunov_"+str(n)+"_"+str(a)+"_"+str(b)+"_"+str(randint(1000000,9999999))+"colour.png")
			
	

	
def createAttractor(img): # https://gist.github.com/mrbichel/1871929
	MAXITERATIONS = 10000000
	NEXAMPLES = 1000
	for n in range(NEXAMPLES):        
		lyapunov = 0
		xmin= 1e32
		xmax=-1e32
		ymin= 1e32
		ymax=-1e32
		ax, ay, x, y = [], [], [], []

		# Initialize coefficients for this attractor
		for i in range(6):
			ax.append(2.0-4.0*random())
			ay.append(2.0-4.0*random())

		# Calculate the attractor
		drawit = True;
		x.append(0.5-random())
		y.append(0.5-random())

		d0 = -1
		while d0 <= 0:
			xe = x[0] + 0.5-random() / 1000.0
			ye = y[0] + 0.5-random() / 1000.0
			dx = x[0] - xe
			dy = y[0] - ye
			d0 = math.sqrt(dx * dx + dy * dy)

		for i in range(MAXITERATIONS):
			# Calculate next term
			
			x.append(ax[0] + ax[1]*x[i-1] + ax[2]*x[i-1]*x[i-1] + ax[3]*x[i-1]*y[i-1] + ax[4]*y[i-1] + ax[5]*y[i-1]*y[i-1])
			y.append(ay[0] + ay[1]*x[i-1] + ay[2]*x[i-1]*x[i-1] + ay[3]*x[i-1]*y[i-1] + ay[4]*y[i-1] + ay[5]*y[i-1]*y[i-1])
			xenew = ax[0] + ax[1]*xe + ax[2]*xe*xe + ax[3]*xe*ye + ax[4]*ye + ax[5]*ye*ye
			yenew = ay[0] + ay[1]*xe + ay[2]*xe*xe + ay[3]*xe*ye + ay[4]*ye + ay[5]*ye*ye

			# Update the bounds 
			xmin = min(xmin,x[i])
			ymin = min(ymin,y[i])
			xmax = max(xmax,x[i])
			ymax = max(ymax,y[i])

			# Does the series tend to infinity
			if xmin < -1e10 or ymin < -1e10 or xmax > 1e10 or ymax > 1e10:
				drawit = False
				print "infinite attractor"
				break

			# Does the series tend to a point
			dx = x[i] - x[i-1]
			dy = y[i] - y[i-1]
			if abs(dx) < 1e-10 and abs(dy) < 1e-10:
				drawit = False
				print "point attractor"
				break
			

			# Calculate the lyapunov exponents
			if i > 1000:
				dx = x[i] - xenew
				dy = y[i] - yenew
				dd = math.sqrt(dx * dx + dy * dy)
				lyapunov += math.log(math.fabs(dd / d0))
				xe = x[i] + d0 * dx / dd
				ye = y[i] + d0 * dy / dd
			
		# Classify the series according to lyapunov
		if drawit:
			if abs(lyapunov) < 10:
				print "neutrally stable"
				drawit = False
			elif lyapunov < 0:
				print "periodic {} ".format(lyapunov)
				drawit = False 
			else:
				print "chaotic {} ".format(lyapunov) 
			
		# Save the image
		if drawit:
			saveAttractor(img,n,ax,ay,xmin,xmax,ymin,ymax,x,y)