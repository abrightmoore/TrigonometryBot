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

def draw(img):
	maze(img)

def maze(img):
	# CONSTANTS
	method = "MAZE"
	print '%s: Started at %s' % (method, time.ctime())
	width = img.size[0]
	depth = img.size[1]
	

	centreWidth = (int)(width / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)
	NOTVISITED = 0
	VISITED = 1
	WALL = 0
	NOWALL = 1
	WALLSIZE = randint(3,16)
	WALLPURGEPERCENT = 0

	WIDTH = int(width/WALLSIZE)
	DEPTH = int(depth/WALLSIZE)
	
	# END CONSTANTS

	cells = zeros((width,depth,7)) #
	
	Q = [] # traversed paths
	
	x = 0
	z = 0
	
	startCell = (x,z)
	
	logger = 0
	
	print '%s: Generating maze at %s, starting at %s %s' % (method, time.ctime(), x, z)
	keepGoing = True
	while keepGoing == True:
		logger = logger +1
		if cells[x,z,0] == NOTVISITED:
			cells[x,z,0] = VISITED
			Q.append( (x,z) )
			
		# Create an iterable list of neighbouring cells that have not yet been visited
		P = []
		for dP in xrange(-1,2):
			if dP != 0:
				d = x+dP
				if d > -1 and d < WIDTH:
					if cells[d,z,0] == NOTVISITED:
						P.append( (d,z,dP,0) )
				d = z+dP
				if d > -1 and d < DEPTH:
					if cells[x,d,0] == NOTVISITED:
						P.append( (x,d,0,dP) )
		
		Plen = len(P)
		if Plen > 0:
#			print 'Choosing a neighbour'
			# Select a cell at random
			(x1,z1,dx,dz) = P[randint(0, Plen-1)]
			# Remove the wall between this cell and the neighbour
			if dx == -1:
				cells[x,z,1] = NOWALL
				cells[x1,z1,2] = NOWALL
			elif dx == 1:
				cells[x,z,2] = NOWALL
				cells[x1,z1,1] = NOWALL
			elif dz == -1:
				cells[x,z,5] = NOWALL
				cells[x1,z1,6] = NOWALL
			elif dz == 1:
				cells[x,z,6] = NOWALL
				cells[x1,z1,5] = NOWALL
			
			# Move along to process the neighbour
			x = x1
			z = z1
			# This is the next cell
		else: # Backtrack
			(x1, z1) = startCell
			if x == x1 and z == z1: #or len(Q) == 0: # We're at the start and there is nowhere else to go
				print 'Generation completed'
				keepGoing = False
			else: # Find me another cell
				if len(Q) > 1:
					(x,z) = Q.pop(randint(1
					,len(Q)-1))
				else:
					print 'Generation completed'
					keepGoing = False
	
	print '%s: Rendering maze at %s' % (method, time.ctime())
	
	colour = (randint(128,255),randint(128,255),randint(128,255),255)
	pix = img.load()
	
	# Now, render unto the maze that which is Caeser's. Draw the walls.
	for iterX in xrange(0,WIDTH):
		for iterZ in xrange(0,DEPTH):
			logger = logger + 1
			if cells[iterX, iterZ, 1] == WALL:
				for iZ in xrange(0,WALLSIZE):
					pix[iterX*WALLSIZE,iterZ*WALLSIZE+iZ] = colour
			if cells[iterX, iterZ, 2] == WALL:
				for iZ in xrange(0,WALLSIZE):
					pix[iterX*WALLSIZE+WALLSIZE-1,iterZ*WALLSIZE+iZ] = colour
			if cells[iterX, iterZ, 5] == WALL:
				for iX in xrange(0,WALLSIZE):
					pix[iterX*WALLSIZE+iX,iterZ*WALLSIZE] = colour
			if cells[iterX, iterZ, 6] == WALL:
				for iX in xrange(0,WALLSIZE):
					pix[iterX*WALLSIZE+iX,iterZ*WALLSIZE+WALLSIZE-1] = colour

	print '%s: Ended at %s' % (method, time.ctime())
