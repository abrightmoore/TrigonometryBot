from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
import sys
from io import BytesIO

from PIL import Image, ImageDraw

def draw(img):
	width = img.size[0]
	height = img.size[1]

	MAX_POINTS = 100000

	IFS_HeighwayDragon = [ (-0.4, 0.0, 0.0, -0.4, -1.0, 0.1, 0.5),
						(0.76, -0.4, 0.4, 0.76, 0.0, 0.0, 0.5)
						] # Note alternate rules should be used for this one


	IFS_BarnsleyFern = [ (0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01),
			(0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07),
			(-0.15,0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
			(0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85)
			]

	IFS_1 = [ (0.0, 0.0, 0.0, 0.6, 0.0,-0.065, 0.1),
			  (0.440,0.0,0.0,0.55,0.0,0.2,0.18),
			  (0.343,-0.248,0.199,0.429,-0.03,0.1,0.18),
			  (0.343,0.248,-0.199,0.429,0.03,0.1,0.18),
			  (0.28,-0.35,0.28,0.35,-0.05,0.0,0.18),
			  (0.28,0.35,-0.28,0.35,0.05,0.0,0.18)
			]

	#    IFS = IFS_generate()

	IFSs = [ IFS_HeighwayDragon, IFS_BarnsleyFern, IFS_1] #, IFS_RAND]

	col1 = (255,255,0,255)
	col2 = (64,16,8,255)
	#IFS = IFS_BarnsleyFern
	IFS = IFSs[randint(0,len(IFSs)-1)]

	for iters in xrange(0,2): # Add more iterations here for ferns
		IFS = IFS_mutate(IFS,0.3*random())
		colour = colourInterpolate(col1,col2,1.0/float(iters+1))
		drawIFS(img,MAX_POINTS,IFS,colour)
	   
	#    colour1 = (128,255,0,255)
	#    colour2 = (255,0,255,255)
	#    colour3 = (0,255,0,255)


	#   drawIFS(img,MAX_POINTS,IFS_1,colour1)
	#   drawIFS(img,MAX_POINTS,IFS_RAND)
	#   drawIFS(img,MAX_POINTS,IFS[0],colour2)
	#   drawIFS(img,MAX_POINTS,IFS[1],colour3)
		
	#   drawIFS(img,MAX_POINTS,IFS[randint(0,len(IFS)-1)])

	return img

def colourInterpolate(col1,col2,distance):
    (r1,g1,b1,a1) = col1
    (r2,g2,b2,a2) = col2
    distance = 1.0-distance
    (r,g,b,a) = (r1+(r2-r1)*distance,g1+(g2-g1)*distance,b1+(b2-b1)*distance,a1+(a2-a1)*distance)
    return (int(r),int(g),int(b),int(a))
        
def IFS_mutate(IFS,degree):
    newIFS = []
    for (a,b,c,d,e,f,p) in IFS:
        gene = randint(1,6)
        if gene == 1:
            a = a+degree*random()*randint(-1,1)
        elif gene == 2:
            b = b+degree*random()*randint(-1,1)
        elif gene == 3:
            c = c+degree*random()*randint(-1,1)
        elif gene == 4:
            d = d+degree*random()*randint(-1,1)
        elif gene == 5:
            e = e+degree*random()*randint(-1,1)
        elif gene == 6:
            f = f+degree*random()*randint(-1,1)
        newIFS.append((a,b,c,d,e,f,p))
    return newIFS

def IFS_generateValue():
    result = 0.0
    chance = random()
    if chance > 0.7:
        result = -1.0+2.0*random() # Distribute term from -1,0 to 1.0
    elif chance > 0.2:
        result = 0.20*random()
#    elif chance > 0.3:
#        result = 0.05*random()

    return result

def IFS_generate():
    probSum = 0.0
    probability = []
    maxRules = randint(2,8)
    for i in xrange(0,maxRules):
        val = random()
        probability.append(val)
        probSum = probSum+val

    probabilitySorted = probability.sort()

    prob = []
    for i in probability:
        prob.append(i/probSum)

    IFS = []

    for i in xrange(0,maxRules):
        a = IFS_generateValue()
        b = IFS_generateValue()
        c = IFS_generateValue()
        d = IFS_generateValue()
        e = IFS_generateValue()
        f = IFS_generateValue()
        p = prob[i]
        IFS.append((a,b,c,d,e,f,p))
    print IFS
    return IFS

def plotPixel(pix,plotColour,x,y):
    ''' Plots a point. Change the method here for different styles
    '''
    pix[x,y] = plotColour
    # print x,y

def plotPixels(img,pixels,offsetx,offsety,quantumx,quantumy):
    width = img.size[0]
    height = img.size[1]
    cw = width>>1
    ch = height>>1

    pix = img.load()
    
    for (x,y,plotColour) in pixels:
        px = (x+offsetx)*quantumx
        py = (y+offsety)*quantumy
        if px >= 0 and py >=0 and px < width and py < height:
            plotPixel(pix,plotColour,int(px),height-int(py)-1)

def drawIFS(img,MAX_POINTS,IFS,plotColour):
#    plotColour = (0,0,0,255)
    width = img.size[0]
    height = img.size[1]
    cw = width>>1
    ch = height>>1
    (x,y) = (1.0,1.0)
    loopCounter = MAX_POINTS
#   pix = img.load()

    ABIGNUM = 999999999.0

    minx = ABIGNUM
    miny = ABIGNUM
    maxx = -ABIGNUM
    maxy = -ABIGNUM

    plots = []
    colours = [ (64,23,8,255),
                (92,49,14,255),
                (128,49,14,255),
                ]
    colIndex = 0
    while loopCounter > 0:
        plotx = x
        ploty = y
        plotColour = colours[colIndex%len(colours)]
        plots.append((x,y,plotColour))
        if plotx < minx:
            minx = plotx
        if plotx > maxx:
            maxx = plotx
        if ploty < miny:
            miny = ploty
        if ploty > maxy:
            maxy = ploty

        choice = random()
        index = 0
        cumulativeProbability = 0
        (newx,newy) = (x,y)
        while index < len(IFS):
            (a,b,c,d,e,f,chance) = IFS[index]
            if chance > -1:
                cumulativeProbability = cumulativeProbability+chance
                if choice <= cumulativeProbability:
                    newx = a*float(x)+b*float(y)+e
                    newy = c*float(x)+d*float(y)+f
                    index = len(IFS) # Break the loop
                    colIndex = index
            elif index%len(IFS) == loopCounter%len(IFS):
                newx = a*float(x)+b*float(y)+e
                newy = c*float(x)+d*float(y)+f
                index = len(IFS) # Break the loop
                colIndex = index
            index = index+1
        (x,y) = (newx,newy)
        loopCounter = loopCounter-1

    # Remap the plots to the available canvas.
    quantumx = abs(float(width)/float(maxx-minx))
    quantumy = abs(float(height)/float(maxy-miny))
    print quantumx,quantumy,minx,maxx,miny,maxy
    if False:
        if quantumy < quantumx:
            quantumx = quantumy
        if quantumx < quantumy:
            quantumy = quantumx
        
    plotPixels(img,plots,-minx,-miny,quantumx,quantumy)