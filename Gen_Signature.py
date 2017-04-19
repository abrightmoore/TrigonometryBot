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
	P = [(11, 29, 0), (11, 29, 0), (34, 29, 0), (23, 52, 0), (23, 52, 0), (21, 41, 0), (31, 40, 0), (31, 51, 0), (31, 52, 0), (29, 46, 0), (38, 41, 0), (41, 46, 0), (34, 45, 0), (35, 51, 0), (42, 53, 0), (45,38, 0), (44, 53, 0), (51, 53, 0), (53, 44, 0), (59, 41, 0), (63, 45, 0), (63, 53, 0), (57, 54, 0), (54, 50, 0), (55, 47, 0), (59, 41, 0), (64, 45, 0), (64, 54, 0), (63, 59, 0), (57, 62, 0), (53, 61,0), (52, 60, 0), (65, 60, 0), (69, 51, 0), (70, 42, 0), (77, 42, 0), (80, 47, 0), (78, 51, 0), (76, 53, 0), (71, 53, 0), (70, 49, 0), (70, 44, 0), (72, 42, 0), (77, 42, 0), (82, 42, 0), (85, 47, 0), (84, 53, 0), (83, 54, 0), (83, 50, 0), (87, 42, 0), (88, 42, 0), (93, 43, 0), (94, 46, 0), (94, 49, 0), (94, 52, 0), (94, 54, 0), (93, 48, 0), (96, 47, 0), (99, 44, 0), (101, 42, 0), (105, 43, 0), (107, 45, 0), (108, 49, 0), (108, 53, 0), (106, 54, 0), (102, 56, 0), (99, 53, 0), (98, 50, 0), (99, 47, 0), (101, 43, 0), (102, 43, 0), (107, 42, 0), (111, 43, 0), (113, 43, 0), (114, 46, 0), (114, 51, 0), (113, 54, 0), (112, 55, 0), (112, 50, 0), (115, 46, 0), (116, 43, 0), (118, 42, 0), (120, 44, 0), (121, 47, 0), (121, 51, 0), (119, 55, 0), (119, 56, 0), (120, 50, 0), (121, 47, 0), (123, 43, 0), (125, 43, 0), (127, 43, 0), (129, 46, 0), (129, 50, 0), (128, 54, 0), (127, 57, 0), (127, 58, 0), (126, 52, 0), (128, 51, 0), (130, 47, 0), (134, 44, 0), (136, 43, 0), (139, 43, 0), (143, 44, 0), (144, 47, 0), (144, 50, 0), (142, 52, 0), (139, 51, 0), (136, 50, 0), (135, 50, 0), (134, 51, 0), (134, 55, 0), (134, 57, 0), (136, 58, 0), (138, 58, 0), (141, 59, 0), (143, 59, 0), (148, 55, 0), (150, 54,0), (151, 49, 0), (152, 43, 0), (152, 37, 0), (152, 32, 0), (152, 29, 0), (151, 43, 0), (149, 44, 0), (146, 44, 0), (145, 42, 0), (146, 41, 0), (150, 41, 0), (152, 43, 0), (154, 43, 0), (156, 44, 0),(160, 45, 0), (160, 50, 0), (158, 54, 0), (158, 57, 0), (156, 56, 0), (158, 50, 0), (159, 49, 0), (163, 45, 0), (163, 43, 0), (163, 47, 0), (164, 49, 0), (167, 48, 0), (169, 45, 0), (170, 44, 0), (172, 44, 0), (174, 47, 0), (172, 51, 0), (172, 53, 0), (171, 55, 0), (173, 56, 0), (178, 57, 0), (181, 53, 0), (183, 47, 0), (183, 45, 0), (182, 45, 0), (182, 50, 0), (181, 54, 0), (180, 57, 0), (178, 59, 0), (176, 61, 0), (173, 61, 0), (166, 62, 0), (162, 62, 0), (144, 61, 0), (128, 60, 0), (118, 60, 0), (108, 59, 0), (95, 58, 0), (82, 56, 0), (75, 57, 0), (70, 59, 0), (69, 61, 0), (73, 63, 0), (77, 62, 0), (82, 62, 0), (86, 62, 0), (90, 60, 0), (87, 58, 0), (82, 58, 0), (78, 59, 0), (75, 60, 0), (75, 61, 0)]

	RAMT = 2
	R = []
	for (x,y,z) in P:
		x = x+randint(-RAMT,RAMT)
		y = y+randint(-RAMT,RAMT)
		R.append((x,y,z))
	
	Q = calcLinesSmooth(4,R)
	pixels = img.load()
	(r1,g1,b1) = (255,255,255)
	
	for (x,y,z) in Q:
		(r2,g2,b2,a) = pixels[x,y]
		pixels[x,y] = ((r1+r2)>>1,(g1+g2)>>1,(b1+b2)>>1,a)
	

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


