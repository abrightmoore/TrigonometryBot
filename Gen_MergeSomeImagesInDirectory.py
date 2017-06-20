# @abrightmoore
# Read every image file in a directory and merge them. Output the result blended image.

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint, random, Random
from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
import pygame, sys
from pygame.locals import *
from io import BytesIO
import imageio
from numpy import *

from Colours import *
from ImageTools import *
			
def addImage(workspace,img):
	width = img.size[0]
	height = img.size[1]
	pix = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pix[x,y]
			#print r,g,b
			workspace[x][y][0] = workspace[x][y][0]+r
			workspace[x][y][1] = workspace[x][y][1]+g
			workspace[x][y][2] = workspace[x][y][2]+b
	del pix
	
def draw(img):
	dir = "images/"
	width = img.size[0]
	height = img.size[1]
	workspace = zeros((width,height,3))
	extension = dir+"image_*.png"
	images = glob.glob(extension)
	if len(images) > 0:
		numImagesProc = 0
		while random() > 0.025 or numImagesProc < 3:
			image = images[randint(0,len(images)-1)]
			print "Processing "+image
			imgIn = Image.open(image)
			sx = imgIn.size[0]
			sy = imgIn.size[1]

			if sx != width or sy != height:
				imgIn = imgIn.resize((width,height), Image.ANTIALIAS)
			
			addImage(workspace,imgIn)
			numImagesProc = numImagesProc + 1
				
		pix = img.load()
		for x in xrange(0,width):
			for y in xrange(0,height):
				r = workspace[x][y][0]/numImagesProc
				g = workspace[x][y][1]/numImagesProc
				b = workspace[x][y][2]/numImagesProc
				pix[x,y] = (int(r),int(g),int(b),255)
				
		del pix
		filename =  "image_blended_"+str(randint(10000000000,99999999999))
		imageNormalize(img)
		img.save("images/"+filename+".png") # cache it

