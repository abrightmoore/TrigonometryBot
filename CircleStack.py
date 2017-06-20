from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint, random, Random
from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
import sys
from io import BytesIO
from numpy import *

from PIL import Image, ImageDraw

class CircleStack:

	def __init__(self, pos, radius, quant):
		(x,y) = pos
		self.x = x
		self.y = y
		self.radius = radius
		self.quant = quant
		
	def draw(self,img,mousepos):
		DRAW = ImageDraw.Draw(img)
		mousex,mousey = mousepos
		(ox,oy) = (self.x,self.y)
		radius = self.radius
		dist = radius
		quant = self.quant
		count = 0
		dx = mousex-ox
		dy = mousey-oy
		an = atan2(dy,dx)
		count = 0
		while radius > quant:
			col = (0,0,0,255)
			dir = 1
			if count%2 == 0:
				dir = 0
				col = (255,255,255,255)
			offset = sin(an)*quant
			offsetx = cos(an)*quant
			offset = dir*int(offset)
			offsetx = dir*int(offsetx)
			DRAW.ellipse((ox-radius+offsetx,oy-radius+offset,ox+radius+offsetx,oy+radius+offset), fill = col, outline = col)
			radius = radius - quant
			count = count +1
	