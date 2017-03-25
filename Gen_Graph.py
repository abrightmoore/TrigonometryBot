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
from Gen_Trigonometry import calcFormula

def draw(img):
	formulaR,formulaG,formulaB = getFormulas()
	makeTrigFuncGraphImage(img,formulaR,formulaG,formulaB)

def makeTrigFuncGraphImage(img,formulaR,formulaG,formulaB): # A 2D height graph
	width = img.size[0]
	height = img.size[1]
 #       img.fill((127,127,127,255))

	a = 255
	cw = width >> 1
	ch = height >> 1
	scale = 1
	scaleDelta = 1
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = float(height*scaleDelta)/256.0       

	drawGraph(img,(250,250,250,255))
	pixels = img.load()
	draw = ImageDraw.Draw(img)        

	prevR = None
	prevG = None
	prevB = None
	
	samples = randint(10,30)
	deltay = int(height/samples)
	y = 0
	while y < height:
		for x in xrange(0,width):
			px = QUANTUMX * float(x-cw)
			r = calcFormula(formulaR,px,y)*127+127
			g = calcFormula(formulaG,px,y)*127+127
			b = calcFormula(formulaB,px,y)*127+127
			if r > 255:
				r = 255
			elif r < 0:
				r = 0
			if g > 255:
				g = 255
			elif g < 0:
				g = 0                                           
			if b > 255:
				b = 255
			elif b < 0:
				b = 0                                           
			pyr = height-QUANTUMY * r-1      
			if pyr >= 0 and pyr < height:
				pixels[int(x),int(pyr)] = (int(r),0,0,int(a))
			pyg = height-QUANTUMY * g-1     
			if pyg >= 0 and pyg < height:
				pixels[int(x),int(pyg)] = (0,int(g),0,int(a))
			pyb = height - QUANTUMY * b-1      
			if pyb >= 0 and pyb < height:
				pixels[int(x),int(pyb)] = (0,0,int(b),int(a))
			if prevR != None: draw.line(prevR+(x,int(pyr)), (int(r),0,0,int(a)))
			if prevG != None: draw.line(prevG+(x,int(pyg)), (0,int(g),0,int(a)))
			if prevB != None: draw.line(prevB+(x,int(pyb)), (0,0,int(b),int(a)))

			prevR = (x,int(pyr))
			prevG = (x,int(pyg))
			prevB = (x,int(pyb))
		y = y + deltay #height/20.0*cos(float(y/height))
	del draw
	del pixels

def drawGraph(img,col):
	width = img.size[0]
	height = img.size[1]
	# img.paste( (0,0,0), [0,0,width,height])

	a = 255
	cw = width >> 1
	ch = height >> 1
	scale = 1
	scaleDelta = 1
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = (2.0*pi)/float(height*scaleDelta)        
	pixels = img.load()
 
	for x in xrange(0,width):
		pixels[x,ch] = col
	for y in xrange(0,height):
		pixels[cw,y] = col
	del pixels