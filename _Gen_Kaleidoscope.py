# Kaleid0scope - inspired by: https://i.imgur.com/pbkgUBv.gifv
# @TheWorldFoundry

# Select a triangular area from an image
# Flip/rotate and replicate it onto a target image.

import sys
from math import atan2,degrees,sqrt
from random import random,randint

from io import BytesIO
import StringIO
import imageio
from numpy import *

import pygame
from pygame import gfxdraw
pygame.init()

from Colours import *
from ImageTools import *

BGCOL = (255,255,255)

def draw(img):
	width = img.size[0]
	height = img.size[1]
	FILENAME = "Kaleidoscope_"+str(randint(10000000000,99999999999))
#	img.save(FILENAME+".png") # Transfer to pygame. This should be possible PIL -> PyGame but...!!!
	mode = img.mode
	size = img.size
	data = img.tobytes()
#	print mode,size
	imgs = img.tobytes("raw",'RGBA')
	imgSource = pygame.image.fromstring(imgs, size, mode)
	imgSource = pygame.transform.scale(imgSource,(width,height) )
#	pygame.image.save(imgSource, FILENAME+"_KaleidoscopeSrc.png")
	#imgSource.convert()
	GAP = 5
#	imgSource = pygame.image.load(FILENAME+".png")
#	height = imgSource.get_width()
#	width = height
	imgTarget = pygame.Surface((width, height))
	#imgTarget.convert()
	imgTarget.set_colorkey((0,0,0))
	# Choose a section of the image
	minSize = height>>6
	maxSize = height>>2
	size = randint(minSize,maxSize)
	sizeY = int(sqrt(size**2 - (size/2)**2))
#	print size,sizeY
	imgFragmentX = randint(0,width-size-1)
	imgFragmentY = randint(0,height-sizeY-1)
	imgFragment = pygame.Surface((size,sizeY))
	#imgFragment.convert()
	imgFragment.set_colorkey((0,0,0))
	imgFragment.blit(imgSource,(0,0,size,sizeY),(imgFragmentX,imgFragmentY,size,sizeY))
	pygame.image.save(imgFragment, "./kaleidoscopefragments/"+FILENAME+"_KaleidoscopeFrag.png")
	# Now we need to mask out only the triangle we care about.
	pointsA = [(0,0),(0,sizeY-1),(size>>1,sizeY-1)]
	pointsA.append(pointsA[0])
	pointsB = [(size-1,0),(size-1,sizeY-1),(size>>1,sizeY-1)]
	pointsB.append(pointsB[0])
	gfxdraw.filled_polygon(imgFragment,pointsA,(0,0,0,255))
  	gfxdraw.filled_polygon(imgFragment,pointsB,(0,0,0,255))
#	pygame.image.save(imgFragment, sys.argv[1]+FILENAME+"_KaleidoscopeFragClip.png")
	imgFragmentFlipped = pygame.transform.flip(imgFragment,False,True)
	angle = degrees(atan2(size>>1,sizeY))*2
	imgFragmentRotate1 = pygame.transform.rotate(imgFragmentFlipped,angle*2)
	imgFragmentRotate1rect = imgFragmentRotate1.get_bounding_rect()
	imgFragmentRotate2 = pygame.transform.rotate(imgFragmentFlipped,angle*4)
	imgFragmentRotate2rect = imgFragmentRotate2.get_bounding_rect()
	imgFragmentRotate3 = pygame.transform.rotate(imgFragment,angle*2)
	imgFragmentRotate3rect = imgFragmentRotate3.get_bounding_rect()
	imgFragmentRotate4 = pygame.transform.rotate(imgFragment,angle*4)
	imgFragmentRotate4rect = imgFragmentRotate4.get_bounding_rect()

	# Now we need to blit this into a hex pattern
	imgFragmentHexTile = pygame.Surface(((size<<1)-GAP,(sizeY<<1)-GAP))
	#imgFragmentHexTile.convert()
	imgFragmentHexTile.set_colorkey((0,0,0))
	x = size>>1
	y = 0
	imgFragmentHexTile.blit(imgFragment,[x,y])
	imgFragmentHexTile.blit(imgFragmentFlipped,[x,y+sizeY-GAP])
	imgFragmentHexTile.blit(imgFragmentRotate1,[x+(size>>1)-GAP,y],imgFragmentRotate1rect)
	#imgFragmentHexTile.blit(imgFragmentRotate1,[x-(size)+GAP,y+sizeY-GAP],imgFragmentRotate1rect)
	imgFragmentHexTile.blit(imgFragmentRotate2,[x-(size>>1)+GAP,y],imgFragmentRotate2rect)
	#imgFragmentHexTile.blit(imgFragmentRotate2,[x+(size)-GAP*2,y+sizeY-GAP],imgFragmentRotate2rect)
	imgFragmentHexTile.blit(imgFragmentRotate3,[x-(size>>1)+GAP,y+sizeY-GAP],imgFragmentRotate3rect)
	#imgFragmentHexTile.blit(imgFragmentRotate3,[x+size-GAP,y],imgFragmentRotate3rect)
	imgFragmentHexTile.blit(imgFragmentRotate4,[x+(size>>1)-GAP,y+sizeY-GAP],imgFragmentRotate4rect)
	#imgFragmentHexTile.blit(imgFragmentRotate4,[x-(size)+GAP*2,y],imgFragmentRotate4rect)
	#pygame.image.save(imgFragmentHexTile, sys.argv[1]+FILENAME+"_KaleidoscopeHexTile.png")
	
	# Now we need to blit this around the screen like a crazy freakazoid

	size = imgFragmentHexTile.get_width()#>>1
	sizeY = imgFragmentHexTile.get_height()#>>1
	x = -size
	y = 0
	while y < height+sizeY:
		while x < width+size:
			imgTarget.blit(imgFragmentHexTile,[x,y])
			imgTarget.blit(imgFragmentHexTile,[x+(size>>2)*3-GAP*2,y-(sizeY>>1)])
			x += size+(size>>1)-GAP*4
		y += (sizeY)-GAP
		x = -size
	
	pix = img.load()
	for y in xrange(0,height):
		for x in xrange(0,width):
			(r,g,b,a) = imgTarget.get_at((x,y))
			pix[x,y] = (r,g,b,a)
	
#	pil_string_image = pygame.image.tostring(imgTarget,"RGBA",False)
#	img = Image.frombytes("RGBA",(1280,720),pil_string_image)

	#img = im
	#mergeImages(img,im,"Circle")
	# print "Blah"
	
#	pygame.image.save(imgTarget, sys.argv[1]+FILENAME+"_KaleidoscopeOut.png")


