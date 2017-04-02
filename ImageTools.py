from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys

from PIL import Image, ImageDraw

def getFormulas():
	formulaR = makeRandomFormula()
	formulaG = makeRandomFormula()
	formulaB = makeRandomFormula()
	return (formulaR,formulaG,formulaB)

def makeRandomFormula():
	result = ""
	funcs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRS"
	iters = randint(1,11)
	for i in xrange(0,iters):
		result=result+(funcs[randint(0,len(funcs)-1)])
	return result

def mergeImages(img1,img2,strategy):
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
	cw = width >>1
	ch = height >>1
	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))
	pix = img.load()
	pix1 = img1.load()
	pix2 = img2.load()
	radius = (width+height)>>2
	rad2 = radius**2
	if strategy == "Circle":
		for x in xrange(0,width):
			dx = cw - x
			distx = dx**2
			for y in xrange(0,height):
				dy = ch - y
				dist = distx + dy**2
				if dist > rad2:
						pix[x,y] = pix2[x,y]
				else: # blend
					(r1,g1,b1,a1) = pix1[x,y]
					(r2,g2,b2,a2) = pix2[x,y]
					ratio = cos(abs(float(dist)/float(rad2)*pi/2))
					# print ratio
					ratioInv = 1.0-ratio
					(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
					if r > 255:
						r = 255
					if g > 255:
						g = 255
					if b > 255:
						b = 255
					pix[x,y] = (int(r),int(g),int(b),int(a))
	if strategy == "Spike":
		for x in xrange(0,width):
			dx = cw - x
			distx = dx**2
			for y in xrange(0,height):
				dy = ch - y
				dist = distx + dy**2
				if dist > rad2:
					pix[x,y] = pix2[(x-gapx)%width2,(y-gapy)%height2]
				else: # blend
					(r1,g1,b1,a1) = pix1[x,y]
					(r2,g2,b2,a2) = pix2[(x-gapx)%width2,(y-gapy)%height2]
					ratio = 1.0-sin(abs(float(dist)/float(rad2)*pi/2))
					# print ratio
					ratioInv = 1.0-ratio
					(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
					if r > 255:
						r = 255
					if g > 255:
						g = 255
					if b > 255:
						b = 255
					pix[x,y] = (int(r),int(g),int(b),int(a))
	if strategy == "Blend":
		for x in xrange(0,width):
			for y in xrange(0,height):
				(r1,g1,b1,a1) = pix1[x,y]
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
	if strategy == "Threshold":
		for x in xrange(0,width):
			for y in xrange(0,height):
				(r1,g1,b1,a1) = pix1[x,y]
				(r2,g2,b2,a2) = pix2[x,y]
				threshold = int((r1+g1+b1)/3)
				ratio = float(threshold/255.0)
				ratioInv = 1.0-ratio
				(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
				if r > 255:
					r = 255
				if g > 255:
					g = 255
				if b > 255:
					b = 255
				pix[x,y] = (int(r),int(g),int(b),int(a))
		
	return img                                        

def checkAverageAlpha(img):
	width = img.size[0]
	height = img.size[1]
	
	pix = img.load()
	val = 0
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pix[x,y]
			val = val + a
	avg = a/(width*height)
	return avg

def circlePic(img):
	width = img.size[0]
	height = img.size[1]
	cw = width>>1
	ch = height>>1
	r2 = cw**2
	pix = img.load()
	for x in xrange(0,width):
		dx = x-cw
		dx2 = dx**2
		for y in xrange(0,height):
			dy = y-ch
			dy2 = dy**2
			if dx2+dy2 > r2:
				(r,g,b,a) = pix[x,y]
				pix[x,y] = (r,g,b,0)
		
def collapseAlpha(img):
	width = img.size[0]
	height = img.size[1]
	
	pix = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pix[x,y]
			pix[x,y] = (r,g,b,255)

	
def imageCarveCircle(img,colour):
	width = img.size[0]
	height = img.size[1]
	cw = width>>1
	ch = height>>1
	radius = (width+height)>>2
	rad2 = radius**2	
	pix = img.load()
	# The strategy here is to iterate over one quadrant and replicate the carve to all four
	for x in xrange(0,cw):
		dx = cw - x
		distx = dx**2
		for y in xrange(0,ch):
			dy = ch - y
			dist = distx + dy**2
			if dist > rad2:
				# The strategy here is to carve all four quadrants
				pix[x,y] = colour
				pix[width-x-1,y] = colour
				pix[x,height-y-1] = colour
				pix[width-x-1,height-y-1] = colour

def imageAvgDiff(img):
	width = img.size[0]
	height = img.size[1]
	pix = img.load()
	imgB = Image.new('RGBA', size=(width-2, height-2), color=(0, 0, 0))
	pixB = imgB.load()
	for x in xrange(1,width-1):
		for y in xrange(1,height-1):
			avgDelta = 0
			(vr,vg,vb,va) = pix[x,y]
			for dx in xrange(-1,2):
				for dy in xrange(-1,2):
					if not (dx == 0 and dy == 0):
						(nr,ng,nb,na) = pix[x+dx,y+dy]
						avgDelta = avgDelta + int(abs(vr+vg+vb-(nr+ng+nb))/3)
			avgDelta = int(avgDelta / 8)
			pixB[x-1,y-1] = (avgDelta,avgDelta,avgDelta,255)
	return imgB
			
def imageBlend(imgA,imgB):
	width = imgA.size[0]
	height = imgA.size[1]
	pixA = imgA.load()
	pixB = imgB.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			(rA,gA,bA,aA) = pixA[x,y]
			(rB,gB,bB,aB) = pixB[x,y]
			pixA[x,y] = ((rA+rB)>>1,(gA+gB)>>1,(bA+bB)>>1,(aA+aB)>>1)

def imageNormalize(img):
	width = img.size[0]
	height = img.size[1]
	max = 0
	min = 255
	pixels = img.load()
	# First scan: get min and max
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pixels[x,y]
			mx = r
			if g > mx:
				mx = g
			if b > mx:
				mx = b
			mn = r
			if g < mn:
				mn = g
			if b < mn:
				mn = b
			
			if mn < min:
				min = mn
			if mx > max:
				max = mx

	# Second... scale values to 0-255
	if (min > 0 or max < 255) and min < max:
		scaler = float(255)/float(max-min)
		shift = -min
		print min,max,scaler,shift
		for x in xrange(0,width):
			for y in xrange(0,height):
				(r,g,b,a) = pixels[x,y]
				pixels[x,y] = (int(float(scaler*(r+shift))),int(float(scaler*(g+shift))),int(float(scaler*(b+shift))),a)
	