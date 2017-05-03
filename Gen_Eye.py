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
			
def draw(img):
	width = img.size[0]
	height = img.size[1]	
	(r1,g1,b1) = (randint(0,128),randint(0,128),randint(128,255))
	
	ox = width>>1
	oy = height>>1
	
	baseCol = randint(192,255)
	circle(img,(ox,oy),ox,(baseCol,baseCol-5,baseCol-20,255))
	circle(img,(ox,oy),ox>>1,(0,0,0,255))
	
	pixels = img.load()
	NUMSEGS = 78
	ang = pi*2.0/NUMSEGS
	jitter = pi*2.0/NUMSEGS/1
	colour = (randint(0,0),randint(0,0),210,255)
	rband = randint(0,40)
	gband = randint(0,40)
	bband = randint(0,40)
	
	for i in xrange(0,randint(3,8)):
		start = random()*pi*2.0
		for j in xrange(0,NUMSEGS):
			blend = False
			(r,g,b,a) = colour
			chance = random()
			if chance < 0.05:
				(r,g,b,a) = (0,100,100,255)
			elif chance < 0.1:
				(r,g,b,a) = (150,100,40,255)
			elif chance < 0.12:
				(r,g,b,a) = (100,40,40,255)
			if random() < 0.15:
				blend = True
			P = []
			angle = start+ang*j
			P.append( ((ox>>2)*cos(angle),(ox>>2)*sin(angle),0) )
			P.append(P[0])

			rad = ((ox>>2)+(ox>>4))
			jitpos = randint(-1,1)*jitter
			P.append( (rad*cos(angle+jitpos),rad*sin(angle+jitpos),0) )

			rad = ((ox>>2)+(ox>>3))
			jitpos = randint(-1,1)*jitter
			P.append( (rad*cos(angle+jitpos),rad*sin(angle+jitpos),0) )
			
			P.append( ((ox>>1)*cos(angle),(ox>>1)*sin(angle),0) )
			P.append(P[len(P)-1])
			Q = calcLinesSmooth(4,P)
			for (x,y,z) in Q:
				px = x+ox
				py = y+oy
				if px >= 0 and px < width and py > 0 and py < height:
					col = (r+randint(-1,1)*randint(0,rband),g+randint(-1,1)*randint(0,gband),b+randint(-1,1)*randint(0,bband),a)		
					if blend == False:
						pixels[px,py] = col
					else:
						(r,g,b,a) = pixels[px,py]
						(r1,g1,b1,a) = col
						pixels[px,py] = ((r+r1)>>1,(g+g1)>>1,(b+b1)>>1,a)
	rband = randint(0,40)
	gband = randint(0,00)
	bband = randint(0,00)
	ang = pi*2.0/(NUMSEGS>>2)
	
	poss = 0
	possan = pi/180
	for i in xrange(0,randint(1,5)):
		start = random()*pi*2.0
		for j in xrange(0,NUMSEGS>>2):
			poss = poss+possan
			if random() > sin(start+poss):
				blend = True
				col = (100,0,0,255)
				P = []
				angle = start+ang*j
#				P.append( ((ox>>1)*cos(angle),(ox>>1)*sin(angle),0) )
				rad = (ox>>1)+(ox>>4)
				jitpos = randint(-1,1)*randint(-NUMSEGS>>4,NUMSEGS>>4)*jitter
				P.append( ((rad)*cos(angle+jitpos),(rad)*sin(angle+jitpos),0) )
				P.append(P[0])
				rad = (ox)-(ox>>3)
				jitpos = randint(-1,1)*randint(-NUMSEGS>>4,NUMSEGS>>4)*jitter
				P.append( ((rad)*cos(angle+jitpos),(rad)*sin(angle+jitpos),0) )

				jitpos = randint(-1,1)*randint(-NUMSEGS>>4,NUMSEGS>>4)*jitter
				P.append( ((ox)*cos(angle+jitpos),(ox)*sin(angle+jitpos),0) )
				P.append(P[len(P)-1])
				Q = calcLinesSmooth(2,P)
				st = randint(0,len(Q)>>1)
				en = len(Q)-1 #randint(len(Q)>>1,len(Q)-1)
				count = 0
				for (x,y,z) in Q:
					if count >= st and count <= en:
						px = x+ox
						py = y+oy
						if px >= 0 and px < width and py > 0 and py < height:
							if blend == False:
								pixels[px,py] = col
							else:
								(r,g,b,a) = pixels[px,py]
								(r1,g1,b1,a) = col
								pixels[px,py] = ((r+r1),(g+g1),(b+b1),a)
					count = count+1
			

						
#	P = []
#	Q = calcLinesSmooth(4,P)

def circle(img,pos,radius,colour):
	width = img.size[0]
	height = img.size[1]	
	(ox,oy) = pos
	(r,g,b,a) = colour
	pixels = img.load()
	rsq = radius**2
	for x in xrange(-radius,radius+1):
		for y in xrange(-radius,radius+1):
			x2 = x**2
			y2 = y**2
			d2 = x2+y2
			# print d2,rsq
			if d2 <= rsq:
				px = x+ox
				py = y+oy
				if px >= 0 and px < width and py > 0 and py < height:
					pixels[px,py] = colour
					#(r2,g2,b2,a) = pixels[px,py]
					#pixels[px,py] = ((r+r2)>>1,(g+g2)>>1,(b+b2)>>1,a) # Blend
	del pixels




