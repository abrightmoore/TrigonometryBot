import sys
from math import *
from random import *

from PIL import Image, ImageDraw

from ImageTools import *

def makeRandomString():
	formulaR,formulaG,formulaB = getFormulas()
	return formulaR+formulaG+formulaB
		

def draw(img):
	width = img.size[0]
	height = img.size[1]	

	controller = makeRandomString()

	scale = randint(1,4)

	(oX,oY) = (width>>1,height>>1)

	coltype = randint(1,3)
	(R,G,B) = (randint(0,255),randint(0,255),randint(0,255))
	widthQ = scale*2.0*pi/width
	heightQ = scale*2.0*pi/height

	pix = img.load()
	for y in xrange(0,height):
		pY = (y-oY)*heightQ
		for x in xrange(0,width):
			pX = (x-oX)*widthQ
			v = int(127+(f(controller,(pX,pY))*127))%0xff
			if coltype == 1:
				R = v
			elif coltype == 2:
				G = v
			elif coltype == 3:
				B = v
			(r,g,b,a) = pix[x,y]
			pix[x,y] = ((r+R)>>1,(g+G)>>1,(b+B)>>1,a)

	del pix
		

def f(controller,pos):
    (x,y) = pos
    err = 0
    val = 1.0
    # Parse each character of the input and adjust the pixel value accordingly
    for c in controller:
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
                        #print "Unable to calculate tan("+str(x)+")"
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

