import sys
# from os.path import isfile, join
import sys
import glob
import time # for timing
# from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *

from PIL import Image, ImageDraw

from ImageTools import *
import ImageFactory

''' This module is for producing procedural images
	Pass in a canvas to be drawn over.
	1. intermediate images are cached to the file system (Note: manual maintenance required. Track file system usage.
	2. final images are cached too
	3. cached images can be selected
	4. the image generator is a python module
	
	Extends work previously done on ABrush
'''

def cacheImage(img):
	pathImages = "images/"
	filename =  pathImages+"image_"+str(randint(10000000000,99999999999))
	img.save(filename+".png") # cache it

def cacheImageRecover():
	extension = "images/*.png"

	# get a list of the available images (from the file system)
	images = glob.glob(extension)
	imageName = images[randint(0,len(images)-1)]
	print "Recovering cached image: "+imageName
	return Image.open(imageName)
	
def makeRandomImage(width,height):

	img = None
	# Recover an image from the cache
	if random() < 0.5:
		try:
			img = cacheImageRecover()
		except:
			print sys.exc_info()

	# Otherwise make a new one
	if img == None:
		img = Image.new('RGBA', size=(width, height), color=(0, 0, 0, 255))

	try:
		drawImageRandom(img)
		# img.save(filename+"_blendtest.png")
		imageNormalize(img)
		if random() > 0.95:
			colour = (0,0,0,0)
			imageCarveCircle(img,colour)
		cacheImage(img)
	except:
		print sys.exc_info()

	return img

def drawImage(canvas,method):
	''' Choose a generator at random from the file system, invoke it, and get an image back in return
	'''

	module = __import__(method)   # theModule[:-3])
	return module.draw(canvas)

count = 1

while(count > 0):
#	count = count-1
	dimension = 10000  #randint(1,8)*100
	val = randint(32,128)
#	img = Image.new('RGBA', size=(dimension, dimension), color=(val, int(val*3/4), int(val*2/3), 255))
	img = Image.new('RGBA', size=(dimension, dimension), color=(0,0,0, 255))
#	img = ImageFactory.makeRandomImage(dimension,dimension)

	method = "Gen_Maze"
	drawImage(img,method)
	drawImage(img,method)
	drawImage(img,method)	
	
	filename =  method+str(randint(1000000000,9999999999))

	# img.save(filename+"_blendtest.png")
	imageNormalize(img)
#	colour = (0,0,0,0)
#	imageCarveCircle(img,colour)
	img.save(filename+"_normalized.png")
#	img = imageAvgDiff(img)
#	imageNormalize(img)
#	img.save(filename+"_edge.png")
