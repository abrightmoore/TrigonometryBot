from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint, random, Random
from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
import pygame, sys
from pygame.locals import *

from Colours import *

#import Palette # @abrightmoore
pygame.init()

def saveSnapshot(surface,prefix):
	filename = prefix+"_"+str(randint(1111111111,9999999999))+".png"
	pygame.image.save(surface,filename)

def choosePalette():
	# Choose a palette
	C = []
	chance = randint(1,10)
	if chance == 1:
		C = getRandomAnalogousColours()
	elif chance == 2:
		C = getRandomComplementaryColours()
	else:
		C = getColoursBrownian(randint(16,64),randint(4,16))
	# Palette chosen
	return C
	
def doit():
	print "By @abrightmoore. Left click places a point, right click removes it. Return for new colours. Space to save the image."
	FPS = 120
	LEFT = 1 # Mouse event
	RIGHT = 3 # Mouse event
	COL_CANVAS = (0,0,0,0)
#	COL_PEN = (4,4,4,255)
	MAXCOL = 96
	SCREENSNAPSHOTNUM = 1000
	# Your code here
	img = pygame.image.load('input.png')
	imgPixels = pygame.PixelArray(img) # Read only, don't worry about locking
	width = img.get_width()
	height = img.get_height()

	# End your code here

	surface = pygame.display.set_mode((width, height)) # A copy of the source image in size
	surface.fill(COL_CANVAS) # Parchment colour to the canvas
	pygame.display.set_caption('COL\ABSketch')

	
	mousex = 0
	mousey = 0
	fpsClock = pygame.time.Clock()
	fpsClock.tick(FPS)
	iterationCount = 0

	# Choose a palette
	C = choosePalette()
	# Palette chosen
		
	P = []
	WLMIN = 8
	WLMAX = 1280
	P.append((width>>1,height>>1,random(),random()*randint(WLMIN,WLMAX)))
	while True: # main game loop
		mouseClicked = False
		iterationCount = iterationCount+1
#		if iterationCount%SCREENSNAPSHOTNUM == SCREENSNAPSHOTNUM>>2:
#			saveSnapshot(surface,"ABSketch_v8_snapshot_"+str(iterationCount)+"_"+str(randint(10000000,90000000))) # Working copy
		
		for event in pygame.event.get():
			if event.type == QUIT:
				print "Shutting down."
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
 				mousex, mousey = event.pos
 			elif event.type == MOUSEBUTTONUP:
				if event.button == LEFT:
 					mousex, mousey = event.pos
					scale = randint(WLMIN,WLMAX)
					P.append((mousex,mousey,random(),random()*scale)) # Add an emitter point
					print "Added a point. Points are now:"
					print P
 					mouseClicked = True
				elif event.button == RIGHT:
					if len(P) > 0:
						print "Deleting last point"
						P.pop() # remove the previous point
						mouseClicked = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print "Saving the image to file"
					saveSnapshot(surface,"ABAnim")
				elif event.key == pygame.K_RETURN:
					C = choosePalette() # New colour scheme
					print "Changing the colours"
					mouseClicked = True
				elif event.key == pygame.K_ESCAPE:
					print "Shutting down."
					pygame.quit()
					sys.exit()
		# Your code here
		if mouseClicked == True or iterationCount == 1: # Processed event, refresh display

			pixels = pygame.PixelArray(surface) # Get a handle on the screen pixels

			for x in xrange(0,width):
				for y in xrange(0,height):
					# For each pixel, what is the intensity here?
					contribution = 0.0
					for (ox,oy,amp,wavelength) in P:
						dx = ox - x
						dy = oy - y
						d = sqrt(dx**2+dy**2)
						contribution = contribution + amp*cos(d/wavelength)
					size = contribution*float(len(C))
					#print size
					(r1,g1,b1) = C[int(abs(float(size)))%len(C)]
					(r2,g2,b2,a) = (r1,g1,b1,255) #pixels[x][y]
					# print r1,g1,b1,r2,g2,b2,a
					pixels[x][y] = ((r1+r2)>>1,(g1+g2)>>1,(b1+b2)>>1,a)
					#print pixels[x,y]

			del pixels # Release pixel lock
			# End Your code here					
			pygame.display.update()

# @abrightmoore - playing around with Python and Pygame

doit()

