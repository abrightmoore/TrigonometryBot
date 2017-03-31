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
import imageio

from ImageTools import *
from Gen_Trigonometry import calcFormula
from Colours import *
import testLineAnimation

def draw(img):
	width = img.size[0]
	height = img.size[1]
	imgs = []
	filename = "imagesTest/movie_"+str(randint(1000000,9999999))+".gif"
	val = randint(150,192)
	colour=(val,int(val*7/8),int(val*5/6),255)
	pen = (0,0,0,255)
#	with imageio.get_writer(filename, mode='I') as writer:
	P = []
	V = []
	delta = 2
	for i in xrange(0,150):
		P.append((randint(0,width-1),randint(0,height-1),randint(32,192)))
		V.append((randint(-1,1)*randint(delta>1,delta),(randint(-1,1)*randint(delta>1,delta)),(randint(-1,1)*randint(delta>1,delta))))

	P.append(P[0])
	P.append(P[1])
	V.append(V[0])
	V.append(V[1])

	for i in xrange(1,1200):
		imgNew = img.copy() #Image.new("RGBA",size=(img.size[0],img.size[1]),color=colour)
		# print(P)
		testLineAnimation.draw(imgNew,P,pen)

#		writer.append_data(imgNew)
		imgs.append(array(imgNew.getdata()).reshape(imgNew.size[0], imgNew.size[1], 4))
		Q = []
		for j in xrange(0,len(P)):
			(x,y,z) = P[j]
			(vx,vy,vz) = V[j]
			nx = vx+x
			ny = vy+y
			nz = vz+z
			Q.append((nx,ny,nz))
		P = Q
	imageio.mimsave(filename, imgs)
