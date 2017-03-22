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


def draw(img):
	formulaR,formulaG,formulaB = getFormulas()
	makeTrigImage(img,formulaR,formulaG,formulaB)

def makeTrigImage(img,formulaR,formulaG,formulaB): # A kind of psychedelic picture based on application of formula across each location on a place.
	width = img.size[0]
	height = img.size[1]

	a = 255
	cw = width>>1
	ch = height>>1
	scale = 0

	scaleDelta = 1
	if False:
		scaleDelta = -randint(1,(width+height)>>3)
		if R.random() > 0.5:
			scaleDelta = -scaleDelta
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = (2.0*pi)/float(height*scaleDelta)

	pixels = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			px = QUANTUMX * float(x-cw)
			py = QUANTUMY * float(y-ch)
		
			r = calcFormula(formulaR,px,py)*127+127
			# print r
			g = calcFormula(formulaG,px,py)*127+127
			b = calcFormula(formulaB,px,py)*127+127
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

			pixels[int(x),int(y)] = (int(r),int(g),int(b),int(a))


def calcFormula(formula,x,y):
	# parse formula, substitute parameters, adjust result
	val = 1.0
	err = 0
	for c in formula:
		if c == "a":
			val = val* sin(y)
		elif c == "b":
			val = val* cos(y)
		elif c == "c":
			try:
				val = val* tan(y)
			except:
				err = err+1
		elif c == "d":
			val = val* sin(x)
		elif c == "e":
			val = val* cos(x)
		elif c == "f":
			try:
				val = val* tan(x)
			except:
				err = err+1
		elif c == "g":
			val = val* sin(x+y)
		elif c == "h":
			val = val* cos(x+y)
		elif c == "i":
			try:
				val = val* tan(x+y)
			except:
				err = err+1
		elif c == "j":
			val = val* sin(x-y)
		elif c == "k":
			val = val* cos(x-y)
		elif c == "l":
			try:
				val = val* tan(x-y)
			except:
				err = err+1
		elif c == "m":
			if y != 0:
				val = val* x/y
		elif c == "n":
			if x != 0:
				val = val* y/x
		elif c == "o":
			val = val* (x-y)
		elif c == "p":
			val = val* (x+y)
		elif c == "q":
			val = val* x*y
		elif c == "r":
			val = val* atan2(y,x)
		elif c == "s":
			val = val* x**2 
		elif c == "t":
			val = val* x**3 
		elif c == "u":
			try:
				val = val* asin(x)
			except:
				err = err+1
		elif c == "v":
			try:
				val = val* acos(x)
			except:
				err = err+1
		elif c == "w":
			try:
				val = val* atan(x)
			except:
				err = err+1
		elif c == "x":
			try:
				val = val* hypot(x,y)
			except:
				err = err+1
		elif c == "y":
			try:
				val = val* acosh(x)
			except:
				err = err+1
		elif c == "z":
			try:
				val = val* asinh(x)
			except:
				err = err+1
		elif c == "A":
			try:
				val = val* atanh(x)
			except:
				err = err+1
		elif c == "B":
			try:
				val = val* cosh(x)
			except:
				err = err+1
		elif c == "C":
			try:
				val = val* sinh(x)
			except:
				err = err+1
		elif c == "D":
			try:
				val = val* tanh(x)
			except:
				err = err+1
		elif c == "E":
			val = val* min(x,y)
		elif c == "F":
			val = val* max(x,y)

		elif c == "G":
			val = val* sin(val)
		elif c == "H":
			val = val* cos(val)
		elif c == "I":
			try:
				val = val* tan(val)
			except:
				err = err+1
		elif c == "J":
			val = val**2
		elif c == "K":
			try:
				val = val* asin(val)
			except:
				err = err+1
		elif c == "L":
			try:
				val = val* acos(val)
			except:
				err = err+1
		elif c == "M":
			try:
				val = val* atan(val)
			except:
				err = err+1
		elif c == "N":
			try:
				val = val* acosh(val)
			except:
				err = err+1
		elif c == "O":
			try:
				val = val* asinh(val)
			except:
				err = err+1
		elif c == "P":
			try:
				val = val* atanh(val)
			except:
				err = err+1
		elif c == "Q":
			try:
				val = val* cosh(x)
			except:
				err = err+1
		elif c == "R":
			try:
				val = val* sinh(val)
			except:
				err = err+1
		elif c == "S":
			try:
				val = val* tanh(val)
			except:
				err = err+1
			
	return val
