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

def draw(img,P,colour):
	width = img.size[0]
	height = img.size[1]
	SMOOTHAMOUNT = 4
	P = calcLinesSmooth(SMOOTHAMOUNT,P)
	P = makePathUnique(P)
	# print P
	pix = img.load()
	(r,g,b,a) = colour
	for (x,y,z) in P:
		if z > 255:
			z = 255
		if z < 0:
			z = 0
		if x >= 0 and x < width and y >= 0 and y < height:
			#print x,y
			pix[x,y] = (r+(z>1),g,b+z,a)

def drawLine(scratchpad, block, p, q ):
	drawLineConstrained(scratchpad, block, p, q, 0 )

def drawLineWithAlpha(scratchpad, block, p, q ):
	drawLineConstrainedWithAlpha(scratchpad, block, p, q, 0 )
	
def drawLineConstrained(pixels, b, p, q, maxLength ):
	(blockID, blockData) = b
	(x,y,z) = p
	(x1,y1,z1) = q
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dy*dy
	distance = sqrt(dz*dz + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dz, sqrt(distHoriz))
		theta = atan2(dy, dx)

		iter = 0
		while iter <= distance:
			setBlock(pixels,(blockID,blockData),((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(theta)*cos(phi)), (int)(z+iter*sin(phi)) ))
			iter = iter+0.5 # slightly oversample because I lack faith.
			
def drawLineConstrainedWithAlpha(pixels, b, p, q, maxLength ):
	(blockID, blockData) = b
	(x,y,z) = p
	(x1,y1,z1) = q
	(r0,g0,b0,a0) = blockID
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			x2 = (int)(x+iter*cos(theta)*cos(phi))
			y2 = (int)(y+iter*sin(phi))
			z2 = (int)(z+iter*sin(theta)*cos(phi))
			(r,g,b,a) = pixels[x2,y2]
			if a > 0:
				a = a-1
			setBlock(pixels,(((r0+r)%0xff,(g0+g)%0xff,(b0+b)%0xff,(a)%0xff),blockData),(x2, y2, z2))
			iter = iter+0.5 # slightly oversample because I lack faith.
			
def chaikinSmoothAlgorithm(P): # http://www.idav.ucdavis.edu/education/CAGDNotes/Chaikins-Algorithm/Chaikins-Algorithm.html
	F1 = 0.25
	F2 = 0.75
	Q = []
	(x0,y0,z0) = (-1,-1,-1)
	count = 0
	for (x1,y1,z1) in P:
		if count > 0: # We have a previous point
			(dx,dy,dz) = (x1-x0,y1-y0,z1-z0)
			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
			Q.append( (x0*F1+x1*F2,y0*F1+y1*F2,z0*F1+z1*F2) )
		else:
			count = count+1
		(x0,y0,z0) = (x1,y1,z1)

	return Q
			
def setBlock(pixels,b,p):
	# (mx,my) = pixels
	(ID,Data) = b
	(x,y,z) = p

	pixels[x,y] = ID
	
def Factorise(number):
	Q = []
	
	n = number
	
	for iter in xrange(1,(int)(n)):
		p = (int)(n/iter)
		if n - (p * iter) == 0:
			if iter not in Q:
				Q.append(iter)
			if p not in Q:
				Q.append(p)
	return Q
		
def makePathUnique(P):
	Q = []
	(prevX,prevY,prevZ) = (int(-1),int(-1),int(-1)) # Dummy
	for (x,y,z) in P:
		if (int(x),int(y),int(z)) != (int(prevX),int(prevY),int(prevZ)):
			Q.append((x,y,z))
			(prevX,prevY,prevZ) = (int(x),int(y),int(z))
#		else: # Debug
#			print "Duplicate discarded: "+str(x)+",	"+str(y)+", "+str(z)
	return Q
	
def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result
	
# Ye Olde GFX Libraries
def cosineInterpolate(a, b, x): # http://www.minecraftforum.net/forums/off-topic/computer-science-and-technology/482027-generating-perlin-noise?page=40000
	ft = pi * x
	f = ((1.0 - cos(ft)) * 0.5)
	ret = float(a * (1.0 - f) + b * f)
	return ret

def cnoise(x,y,z):
	# Return the value of interpolated noise at this location
	return float(Random(x+(y<<4)+(z<<8)).random())

def noise(x,y,z):
	ss = 8
	bs = 3
	cx = x >> bs
	cy = y >> bs
	cz = z >> bs

	rdx = float((float(x%ss))/ss)
	rdy = float((float(y%ss))/ss)
	rdz = float((float(z%ss))/ss)
#	print rdx,rdy,rdz
	
	# current noise cell
	P = zeros((2,2,2))
	for iy in xrange(0,2):
		for iz in xrange(0,2):
			for ix in xrange(0,2):
				P[ix,iy,iz] = float(cnoise(cx+ix,cy+iy,cz+iz))
	
	# print P

	dvx1 = cosineInterpolate(P[0,0,0],P[1,0,0],rdx)
	dvx2 = cosineInterpolate(P[0,1,0],P[1,1,0],rdx)
	dvx3 = cosineInterpolate(P[0,0,1],P[1,0,1],rdx)
	dvx4 = cosineInterpolate(P[0,1,1],P[1,1,1],rdx)

	dvz1 = cosineInterpolate(dvx1,dvx3,rdz)
	dvz2 = cosineInterpolate(dvx2,dvx4,rdz)

	n = cosineInterpolate(dvz1,dvz2,rdy)
	
	return n

def drawTriangle(level, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def drawTriangleEdge(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge):
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def calcLine((x,y,z), (x1,y1,z1) ):
	return calcLineConstrained((x,y,z), (x1,y1,z1), 0 )
			
def calcLinesSmooth(SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = calcLines(P)
	return flatten(Q)

def calcLines(P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( calcLine((x0,y0,z0),(x,y,z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q
	
def calcLineConstrained((x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			# setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points calc'd
