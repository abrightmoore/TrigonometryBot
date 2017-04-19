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

#import Palette # @abrightmoore
pygame.init()

def saveSnapshot(surface,prefix):
	filename = prefix+"_"+str(randint(1111111111,9999999999))+".png"
	pygame.image.save(surface,filename)

def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result

def calcLinesSmooth(SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = calcLines(P)
	return flatten(Q)

def calcLines(P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( calcLine((x0,y0,z0),(x,y,z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q

def calcLine((x,y,z), (x1,y1,z1) ):
	return calcLineConstrained((x,y,z), (x1,y1,z1), 0 )

def calcLineConstrained((x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			# setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points calc'd
	
def chaikinSmoothAlgorithm(P): # http://www.idav.ucdavis.edu/education/CAGDNotes/Chaikins-Algorithm/Chaikins-Algorithm.html
	F1 = 0.25
	F2 = 0.75
	Q = []
	(x0,y0,z0) = (-1,-1,-1)
	count = 0
	for (x1,y1,z1) in P:
		if count > 0: # We have a previous point
			(dx,dy,dz) = (x1-x0,y1-y0,z1-z0)
			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
			Q.append( (x0*F1+x1*F2,y0*F1+y1*F2,z0*F1+z1*F2) )
		else:
			count = count+1
		(x0,y0,z0) = (x1,y1,z1)

	return Q
	
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
	COL_MARK = (192,0,0,255)
	SMOOTHAMOUNT = 4
	SHOWMARKS = True
	RANDOMISE = False
	RAMT = 8
	imgs = []
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
		
#	P = [(45, 308, 0), (45, 308, 0), (139, 308, 0), (93, 400, 0), (93, 400, 0), (85, 357, 0), (126, 352, 0), (126, 398, 0), (126, 402, 0), (118, 376, 0), (153, 359, 0), (164, 379, 0), (137, 372, 0), (141, 399, 0), (170, 405, 0), (182, 347, 0), (177, 407, 0), (204, 407, 0), (215, 368, 0), (237, 356, 0), (254, 372, 0), (255, 406, 0), (229, 409, 0), (219, 393, 0), (220, 380, 0), (236, 357, 0), (257, 372, 0), (257, 408, 0), (253, 429, 0), (230, 443, 0), (215, 439, 0), (209, 434, 0), (263, 433, 0), (276, 398, 0), (283, 361, 0), (308, 362, 0), (321, 380, 0), (314, 396, 0), (304, 407, 0), (286, 404, 0), (280, 388, 0), (283, 369, 0), (289, 363, 0), (309, 363, 0), (331, 363, 0), (340, 380, 0), (336, 404, 0), (334, 410, 0), (332, 393, 0), (350, 362, 0), (353, 362, 0), (372, 365, 0), (379, 376, 0), (379, 391, 0), (378, 400, 0), (376, 409, 0), (372, 386, 0), (385, 380, 0), (396, 368, 0), (405, 363, 0), (420, 365, 0), (430, 373, 0), (432, 388, 0), (434, 404, 0), (424, 411, 0), (410, 416, 0), (397, 407, 0), (395, 392, 0), (396, 382, 0), (405, 366, 0), (411, 365, 0), (429, 363, 0), (445, 367, 0), (455, 366, 0), (458, 378, 0), (458, 397, 0), (452, 409, 0), (450, 415, 0), (449, 394, 0), (462, 379, 0), (466, 367, 0), (473, 362, 0), (482, 369, 0), (485, 383, 0), (484, 397, 0), (478, 413, 0), (478, 418, 0), (482, 393, 0), (484, 383, 0), (494, 366, 0), (500, 364, 0), (509, 364, 0), (517, 377, 0), (517, 394, 0), (513, 409, 0), (511, 420, 0), (511, 424, 0), (505, 402, 0), (512, 397, 0), (522, 383, 0), (537, 370, 0), (544, 364, 0), (556, 367, 0), (573, 371, 0), (577, 380, 0), (577, 394, 0), (568, 401, 0), (558, 397, 0), (544, 395, 0), (542, 395, 0), (538, 399, 0), (536, 412, 0), (539, 420, 0), (545, 424, 0), (555, 427, 0), (565, 430, 0), (573, 428, 0), (592, 415, 0), (600, 408, 0), (607, 391, 0), (610, 365, 0), (610, 340, 0), (610, 323, 0), (611, 311, 0), (607, 364, 0), (596, 369, 0), (587, 369, 0), (580, 362, 0), (585, 358, 0), (600, 357, 0), (608, 364, 0), (617, 364, 0), (625, 369, 0), (641, 374, 0), (643, 392, 0), (634, 408, 0), (634, 420, 0), (625, 416, 0), (633, 395, 0), (639, 391, 0), (655, 374, 0), (654, 367, 0), (653, 383, 0), (659, 389, 0), (668, 386, 0), (678, 375, 0), (681, 370, 0), (689, 368, 0), (699, 380, 0), (690, 396, 0), (688, 405, 0), (687, 413, 0), (695, 417, 0), (714, 420, 0), (725, 405, 0), (734, 382, 0), (733, 373, 0), (729, 374, 0), (728, 392, 0), (725, 409, 0), (722, 421, 0), (714, 431, 0), (707, 436, 0), (693, 439, 0), (667, 440, 0), (649, 442, 0), (612, 441, 0), (581, 442, 0), (536, 443, 0), (460, 441, 0), (402, 439, 0), (334, 439, 0), (287, 438, 0), (249, 445, 0), (225, 447, 0), (190, 447, 0), (170, 437, 0), (122, 431, 0), (82, 427, 0), (55, 426, 0), (26, 427, 0), (15, 434, 0), (14, 443, 0), (27, 448, 0)]
	# Points to draw
	P = [(45, 116, 0), (45, 116, 0), (139, 116, 0), (93, 208, 0), (93, 208, 0), (85, 165, 0), (126, 160, 0), (126, 206, 0), (126, 210, 0), (118, 184, 0), (153, 167, 0), (164, 187, 0), (137, 180, 0), (141, 207
, 0), (170, 213, 0), (182, 155, 0), (177, 215, 0), (204, 215, 0), (215, 176, 0), (237, 164, 0), (254, 180, 0), (255, 214, 0), (229, 217, 0), (219, 201, 0), (220, 188, 0), (236, 165, 0), (257, 180, 0),
 (257, 216, 0), (253, 237, 0), (230, 251, 0), (215, 247, 0), (209, 242, 0), (263, 241, 0), (276, 206, 0), (283, 169, 0), (308, 170, 0), (321, 188, 0), (314, 204, 0), (304, 215, 0), (286, 212, 0), (280
, 196, 0), (283, 177, 0), (289, 171, 0), (309, 171, 0), (331, 171, 0), (340, 188, 0), (336, 212, 0), (334, 218, 0), (332, 201, 0), (350, 170, 0), (353, 170, 0), (372, 173, 0), (379, 184, 0), (379, 199
, 0), (378, 208, 0), (376, 217, 0), (372, 194, 0), (385, 188, 0), (396, 176, 0), (405, 171, 0), (420, 173, 0), (430, 181, 0), (432, 196, 0), (434, 212, 0), (424, 219, 0), (410, 224, 0), (397, 215, 0),
 (395, 200, 0), (396, 190, 0), (405, 174, 0), (411, 173, 0), (429, 171, 0), (445, 175, 0), (455, 174, 0), (458, 186, 0), (458, 205, 0), (452, 217, 0), (450, 223, 0), (449, 202, 0), (462, 187, 0), (466
, 175, 0), (473, 170, 0), (482, 177, 0), (485, 191, 0), (484, 205, 0), (478, 221, 0), (478, 226, 0), (482, 201, 0), (484, 191, 0), (494, 174, 0), (500, 172, 0), (509, 172, 0), (517, 185, 0), (517, 202
, 0), (513, 217, 0), (511, 228, 0), (511, 232, 0), (505, 210, 0), (512, 205, 0), (522, 191, 0), (537, 178, 0), (544, 172, 0), (556, 175, 0), (573, 179, 0), (577, 188, 0), (577, 202, 0), (568, 209, 0),
 (558, 205, 0), (544, 203, 0), (542, 203, 0), (538, 207, 0), (536, 220, 0), (539, 228, 0), (545, 232, 0), (555, 235, 0), (565, 238, 0), (573, 236, 0), (592, 223, 0), (600, 216, 0), (607, 199, 0), (610
, 173, 0), (610, 148, 0), (610, 131, 0), (611, 119, 0), (607, 172, 0), (596, 177, 0), (587, 177, 0), (580, 170, 0), (585, 166, 0), (600, 165, 0), (608, 172, 0), (617, 172, 0), (625, 177, 0), (641, 182
, 0), (643, 200, 0), (634, 216, 0), (634, 228, 0), (625, 224, 0), (633, 203, 0), (639, 199, 0), (655, 182, 0), (654, 175, 0), (653, 191, 0), (659, 197, 0), (668, 194, 0), (678, 183, 0), (681, 178, 0),
 (689, 176, 0), (699, 188, 0), (690, 204, 0), (688, 213, 0), (687, 221, 0), (695, 225, 0), (714, 228, 0), (725, 213, 0), (734, 190, 0), (733, 181, 0), (729, 182, 0), (728, 200, 0), (725, 217, 0), (722
, 229, 0), (714, 239, 0), (707, 244, 0), (693, 247, 0), (667, 248, 0), (649, 250, 0), (577, 245, 0), (514, 243, 0), (472, 242, 0), (432, 238, 0), (381, 232, 0), (328, 227, 0), (300, 230, 0), (283, 236
, 0), (277, 247, 0), (292, 253, 0), (308, 250, 0), (331, 248, 0), (345, 248, 0), (362, 243, 0), (348, 235, 0), (329, 235, 0), (315, 237, 0), (302, 240, 0), (293, 242, 0), (191, 260, 0)]	
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
					P.append((mousex,mousey,0)) # Add an emitter point
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
				elif event.key == pygame.K_UP:
					Q = []
					for (x,y,z) in P:
						Q.append((x,y-RAMT,z))
					P = Q
					mouseClicked = True
				elif event.key == pygame.K_DOWN:
					Q = []
					for (x,y,z) in P:
						Q.append((x,y+RAMT,z))
					P = Q
					mouseClicked = True
				elif event.key == pygame.K_LEFT:
					Q = []
					for (x,y,z) in P:
						Q.append((x-RAMT,y,z))
					P = Q
					mouseClicked = True
				elif event.key == pygame.K_RIGHT:
					Q = []
					for (x,y,z) in P:
						Q.append((x+RAMT,y,z))
					P = Q
					mouseClicked = True

				elif event.key == pygame.K_SLASH:
					Q = []
					for (x,y,z) in P:
						Q.append((x>>1,y>>1,z))
					P = Q
					mouseClicked = True
				elif event.key == pygame.K_BACKSLASH:
					Q = []
					for (x,y,z) in P:
						Q.append((x<<1,y<<1,z))
					P = Q
					mouseClicked = True
				elif event.key == pygame.K_0:
					RANDOMISE = True
					mouseClicked = True
				elif event.key == pygame.K_1:
					RANDOMISE = False
					imgs = []
					mouseClicked = True
				elif event.key == pygame.K_MINUS:
					SHOWMARKS = False
					mouseClicked = True
				elif event.key == pygame.K_EQUALS:
					SHOWMARKS = True
					mouseClicked = True
				elif event.key == pygame.K_BACKSPACE:
					P = []
					print 'Erase all points'
					mouseClicked = True
				elif event.key == pygame.K_i:
					filename = "Scribble_"+str(randint(1000000,9999999))+".gif"
					imgsNumpy = []
					for image in imgs:
						#imgsNumpy.append(array(image.getdata()).reshape(image.size[0], image.size[1], 4))
						imgsNumpy.append(image)
					imageio.mimsave(filename, imgsNumpy)
				elif event.key == pygame.K_ESCAPE:
					print "Shutting down."
					pygame.quit()
					sys.exit()
		# Your code here
		if mouseClicked == True or iterationCount == 1 or RANDOMISE == True: # Processed event, refresh display
			surface.fill(COL_CANVAS)
			R = P
			if RANDOMISE == True:
				Q = []
				for (x,y,z) in P:
					x = x+randint(-RAMT,RAMT)
					y = y+randint(-RAMT,RAMT)
					Q.append((x,y,z))
				R = Q
			Q = calcLinesSmooth(SMOOTHAMOUNT,R)
			pixels = pygame.PixelArray(surface) # Get a handle on the screen pixels

			for (x,y,z) in Q:
				(r1,g1,b1) = C[0]
				pixels[x][y] = (r1,g1,b1,255)
			if SHOWMARKS == True:
				for (x,y,z) in P:
					pixels[x-1][y] = COL_MARK
					pixels[x][y] = COL_MARK
					pixels[x+1][y] = COL_MARK
					pixels[x][y-1] = COL_MARK
					pixels[x][y+1] = COL_MARK


			if RANDOMISE == True:
			#	data = pygame.image.tostring(surface, 'RGBA')
			#	img = Image.frombytes('RGBA', (width,height), frame)
			#	img = pygame.image.fromstring(data, (width,height), 'RGBA')
				frame = zeros((height,width))
				for x in xrange(0,width):
					for y in xrange(0,height):
						frame[y,x] = pixels[x][y]
				imgs.append(frame)
			# End Your code here					
			del pixels # Release pixel lock
			pygame.display.update()

# @abrightmoore - playing around with Python and Pygame

doit()

