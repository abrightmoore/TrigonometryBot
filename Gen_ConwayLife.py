# @abrightmoore
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
	SAVEANIMATION = False # Make this True to create an animated file. Warning: large.
	imgs=alife(img,randint(20,80))
	filename = "imagesTest/ablife_"+str(randint(1000000,9999999))+".gif"
	imgsNumpy = []
	for image in imgs:
		imgsNumpy.append(array(image.getdata()).reshape(image.size[0], image.size[1], 4))
	if SAVEANIMATION == True:
		imageio.mimsave(filename, imgsNumpy)
	imageBlend(img,imgs[len(imgs)-1])

def randomise(field,chance):
	(width,height) = field.shape
	
	for x in xrange(0,width):
		for y in xrange(0,height):
			if randint(1,100) <= chance:
				field[x][y] = 1
			else:
				field[x][y] = 0

def doILiveOrDie(self,neighbours):
	''' Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
		Any live cell with two or three live neighbours lives on to the next generation.
		Any live cell with more than three live neighbours dies, as if by overpopulation.
		Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
		'''
	DEAD = 0
	ALIVE = 1
	
	if neighbours == 3:
		return ALIVE
	if neighbours == 0 or neighbours == 1:
		return DEAD
	if neighbours == 2 and self != DEAD:
		return ALIVE
#if neighbours > 3:
	return DEAD
				
def alife(img,iters):
	width = img.size[0]
	height = img.size[1]
	BGCOLOUR = (192,184,164,255)
	frames = [] # consecutive iterations of the function
	
	cellSize = randint(1,int(width/16))
	numCellRows = int(height/cellSize)
	numCellCols = int(width/cellSize)
	
	thisField = zeros((numCellCols,numCellRows)) # x/y
	chance = randint(40,60)
	randomise(thisField,chance) # seed
	strategy = randint(1,6)
	filename = "imagesTest/alife_"+str(randint(1000000000,9999999999))+"_"
	for i in xrange(0,iters):
		nextField = zeros((numCellCols,numCellRows)) # x/y
		# loop through thisField, calculate survivors to nextField
		for x in xrange(0,numCellCols):
			for y in xrange(0,numCellRows):
				# with toroidal wrapping at edges, count the number of neighbours
				neighbours = 0
				for ix in xrange(-1,2):
					for iy in xrange(-1,2):
						if not (ix == 0 and iy == 0): # Don't count myself
							px = (x+ix)%numCellCols # Wrap edges
							py = (y+iy)%numCellRows # Wrap edges
							if thisField[px][py] != 0:
								neighbours = neighbours+1
				
				# Now work out what happens next generation to this cell based on neighbour count
				nextField[x][y] = doILiveOrDie(thisField[x][y],neighbours)
		# render nextField to the new image
		newImg = drawFrame(img, nextField, cellSize, BGCOLOUR, strategy)
#		newImg.save(filename+str(i)+".png")
		frames.append(newImg)
		
		copyFields(thisField,nextField)

	print len(frames)
	return frames # Maybe think about adding the first one too? Too messy from random though?

def drawFrame(img, nextField, cellSize, BGCOLOUR, strategy):
	width = img.size[0]
	height = img.size[1]
	numCellRows = int(height/cellSize)
	numCellCols = int(width/cellSize)
	nextFrame = Image.new("RGBA",size=(img.size[0],img.size[1]),color=BGCOLOUR)
	nextPix = nextFrame.load()
	pix = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			px = int(x/cellSize)
			py = int(y/cellSize)
			if nextField[px%numCellCols][py%numCellRows] == 1:
				(r,g,b,a) = pix[x,y]
				if strategy == 1:
					val = int((r+g+b)/3)
					(r,g,b,a) = (val,val,val,255)
				elif strategy == 2:
					(r,g,b,a) = (255-r,255-g,255-b,255)
				elif strategy == 3:
					val = int((r+g+b)/3)
					(r,g,b,a) = (255-val,255-val,255-val,255)
				elif strategy == 4:
					(r,g,b,a) = (b,r,g,255)
				elif strategy == 5:
					(r,g,b,a) = (255,255,255,255)
				elif strategy == 6:
					(r,g,b,a) = (randint(0,255),randint(0,255),randint(0,255),255)
				else:
					(r,g,b,a) = (0,0,0,255)
				nextPix[x,y] = (r,g,b,a) # Copy this pixel from source
			else:
				nextPix[x,y] = pix[x,y]
	return nextFrame
	
def copyFields(toField,fromField):
	(numCellCols,numCellRows) = toField.shape
	for x in xrange(0,numCellCols):
		for y in xrange(0,numCellRows):
			toField[x][y] = fromField[x][y]

	