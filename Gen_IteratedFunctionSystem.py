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

	IFS_ANCHORS = [
					(0.0, 0.10, 0.0, 0.40, -0.002, 0.0, 0.08),
					(0.7, 0.135,     -0.235,    0.7,       -0.2,     0.01,   0.45),
					(0.121328,   -0.120,      0.230,    0.32318,    0.01,    0.01,   0.25),
					(0.121328,    0.34330,    0.240,    0.218,      0.0,     0.01,   0.22)
				]
	IFS_ANGLES = [ (0.5, 0.0, 0.0, 0.5, -4.5, 0.002, 0.33),
					(0.5, 0.0, 0.0, 0.5, 4.6, 0.002, 0.33),
					(0.32139, 0.38302, -0.38302, 0.32139, 1.09, 9.5, 0.33)
	]
	
	IFS_BABYLON = [(0.0,-0.5,0.85,0.0,-1.732366,3.366182,0.333333),
					(0.3,0.0,0.0,0.3,-0.027891,5.014877,0.333333),
					(0.0,0.5,-0.85,0.0,1.620804,3.310401,0.333334)
					]
	
	IFS_CASTLE = [(0.5,0.0,0.0,0.5,0,0,0.25),
					(0.5,0.0,0.0,0.5,3,0,0.25),
					(0.4,0.0,0.0,0.4,0,2,0.25),
					(0.5,0.0,0.0,0.5,3,2,0.25)
				]
	IFS_CLOUD = [
					(0.25000,0.00000,0.00000,0.25000,0.00000,0.00000,.17),
					(0.25000,-0.25000,0.25000,0.25000,0.25000,0.00000,.17),
					(0.50000,0.50000,-0.50000,0.50000,0.50000,0.25000,.16),
					(0.50000,0.50000,-0.50000,0.50000,0.25000,0.00000,.16),
					(0.25000,-0.25000,0.25000,0.25000,0.50000,-0.25000,.17),
					(0.25000,0.00000,0.00000,0.25000,0.75000,0.00000,.17)
	]
	
	IFS_CORAL = [
					(-0.16666667,-0.1666667,0.16666667,-0.1666667,0.0000000,0.000000,0.163),
					 (0.83333333,0.2500000,-0.25000000,0.8333333,-0.1666667,-0.166667,0.600),
					 (0.33333333,-0.0833333,0.08333333,0.3333333,0.0833333,0.666667,0.237)
	]
	
	IFS_CORAL1 = [
					(0.307692,-0.531469,-0.461538,-0.293706,5.401953,8.655175,0.40),
					(0.307692,-0.076923,0.153846,-0.447552,-1.295248,4.152990,0.15),
					(0.000000,0.545455,0.692308,-0.195804,-4.893637,7.269794,0.45)
	]
	
	IFS_COSMOS = [
					(0.4578,-0.491,0.61,0.911,1.479,0.692,0.9175),
					(0.56,0.3,-0.5,0.9,0.64,0.5,0.5)
	]
	
	IFS_CRYSTAL = [
					(0.696970,-0.481061,-0.393939,-0.662879,2.147003,10.310288,0.747826),
					(0.090909,-0.443182,0.515152,-0.094697,4.286558,2.925762,0.252174)
	]

	IFS_CRYSTAL4 = [
					(0.1767,-0.7071,0.7071,0.1767,0.0000,0.0000,0.25),
					(-0.1767,0.7071,-0.7071,-0.1767,0.0000,0.0000,0.25),
					(0.5000,0.0000,0.0000,0.5000,0.5000,0.0000,0.50)
	]
	
	IFS_CURL = [
				(.693,.400,-.400,.693,0,0,.85),
				(.346,-.200,.200,.346,.693,.400,.15)
	]
	
	IFS_DOGS = [
				(0.8517,-0.3736,0.3736,0.7517,0.0000,0.000,0.7),
				(0.3000,0.1000,-0.1000,0.2000,1.0000,-0.364,0.1),
				(0.3000,0.1000,-0.1000,0.2000,-0.3640,1.000,0.1),
				(0.3000,0.1000,-0.0000,0.2000,-0.7280,-0.728,0.1)	
	]
	
	IFS_DRAGON1 = [
					(0.824074,0.281482,-0.212346,0.864198,-1.882290,-0.110607,0.787473),
					(0.088272,0.520988,-0.463889,-0.377778,0.785360,8.095795,0.212527)
	]
	
	IFS_DRAGON2 = [
					(0.824074,0.581482,-0.212346,0.864198,1.882290,0.110607,0.787473),
					(0.088272,0.420988,-0.463889,-0.377778,0.785360,8.095795,0.212528)
	]
	
	IFS_FERN1 = [
					(0.0,0.0,0.0,0.22,0.0,0.0,0.01),
					(0.8,0.135,-0.235,0.8,0.0,1.4,0.49),
					(0.15,-0.120,0.130,0.12,0.0,1.0,0.25),
					(0.15,0.200,0.340,0.12,0.0,0.5,0.25)
	]
	
	IFS_FLOOR = [
					(0.0,-0.5,0.5,0.0,.25,-.25,0.333333),
					(0.5,0.0,0.0,0.5,.25,.25,0.333333),
					(0.0,0.5,-0.5,0.0,.75,.25,0.333334)
	]
	
	IFS_FLOOR1 = [
					(0.5,0.0,0.0,0.5,-2.563477,-0.000003,0.333333),
					(0.5,0.0,0.0,0.5,2.436544,-0.000003,0.333333),
					(0.0,-0.5,0.5,0.0,4.873085,7.563492,0.333333)
	]
	
	IFS_FLOOR2 = [
					(.333,0,0,.333,.333,.666,.2),
					(0,.333,1,0,.666,0,.4),
					(0,-.333,1,0,.333,0,.4)
	]

	IFS_FLYFISH = [
					 (0.2,-0.5,0.5,-0.5,.9,.5,0.5),
					 (0.8,0.5,-0.5,0.5,.9,.5,0.5)
	]
	
	IFS_LEAF = [
					 (0.555,0.000,0.000,0.555,0.000,0.000,0.20),
					 (0.550,0.000,0.000,0.550,0.000,0.185,0.30),
					 (0.353,0.281,-0.295,0.336,0.068,0.112,0.25),
					 (0.353,-0.281,0.295,0.336,-0.068,0.112,0.25)
	]
	
	IFS_LEAF2 = [
					(0.3333,0.0,0.0,0.3333,0.0,0.0,0.1667),
					(0.1667,-0.2887,0.2887,0.1667,0.3333,0.0,0.1667),
					(0.1667,-0.2887,0.2887,0.1667,0.0833,0.0,0.1667),
					(0.1667,0.2887,-0.2887,0.1667,0.3333,0.0,0.1667),
					(0.1667,0.2887,-0.2887,0.1667,0.0833,0.0,0.1667),
					(0.3333,0.0,0.0,0.3333,0.6667,0.0,0.1667)	
	]
	
	IFS_POSIES2 = [
					 (0.2500,0.2500,-0.2500,0.2500,0.0000,0.0000,0.25),
					 (0.5000,-0.5000,0.5000,0.5000,0.2500,0.2500,0.50),
					 (0.2500,0.2500,-0.2500,0.2500,0.7500,-0.2500,0.25)
	]
	
	IFS_SATDISH = [
					(0.5,0.0,0.0,0.5,0.0,0.0,.33),
					(0.0,-0.5,0.5,0.0,0.5,0.0,.33),
					(0.5,0.0,0.0,0.5,0.5,0.5,.34)
	]
	
	IFS_SPIRAL = [
					 (0.787879,-0.424242,0.242424,0.859848,1.758647,1.408065,0.895652),
					 (-0.121212,0.257576,0.090909,0.053030,-3.721654,1.377236,0.052174),
					 (0.252525,-0.136364,0.252525,0.181818,3.086107,1.568035,0.052174)
	]
	
	IFS_SPIRAL1 = [
					(0.7517,-0.2736,0.2736,0.7517,0.0000,0.000,0.7),
					(0.2000,0.0000,0.0000,0.2000,1.0000,-0.364,0.1),
					(0.2000,0.0000,0.0000,0.2000,-0.3640,1.000,0.1),
					(0.2000,0.0000,0.0000,0.2000,-0.7280,-0.728,0.1)
	]
	
	IFS_SPIRAL2 = [
					(0.787879,-0.424242,0.242424,0.859848,1.758647,1.408065,0.895652),
					(-0.121212,0.257576,0.151515,0.053030,-6.721654,1.377236,0.052174),
					(0.181818,-0.136364,0.090909,0.181818,6.086107,1.568035,0.052174)
	]
	
	IFS_SPIRAL3 = [
					(0.745455,-0.459091,0.406061,0.887121,1.460279,0.691072,0.85),
					(-0.424242,-0.065152,-0.175758,0.218182,3.809567,6.741476,0.15)
	]
	
	IFS_STICKS = [
					(0.005,0.000,0.000,0.500,0.0,0.0,0.12),
					(0.414,-0.414,0.414,0.414,0.0,0.5,0.44),
					(0.414,0.414,-0.414,0.414,0.0,0.5,0.44)
	]
	
	IFS_SWIRL = [
					(0.745455,-0.459091,0.406061,0.887121,1.460279,0.691072,0.912675),
					(-0.424242,-0.065152,-0.175758,-0.218182,3.809567,6.741476,0.087325)
	]
	
	IFS_TOWER = [
					(0.75,0.00,0.00,0.30,-0.20,0.00,0.23),
					(0.75,0.00,0.00,0.30,0.20,0.00,0.23),
					(0.50,0.00,0.00,0.80,0.00,0.20,0.54)
	]
	
	IFS_TREE = [
					(0.195,-0.488,0.344,0.443,0.722,0.536,0.4),
					(0.462,0.414,-0.252,0.361,0.538,1.167,0.4),
					(-0.058,-0.070,0.453,-0.111,1.125,0.185,0.1),
					(-0.045,0.091,-0.469,-0.022,0.863,0.871,0.1)
	]
	
	IFS_TREE1 = [
					(.195,-.488,.344,.443,.4431,.2452,.2),
					(.462,.414,-.252,.361,.2511,.5692,.25),
					(-.058,-.070,.453,-.111,.5976,.0969,.2),
					(-.035,.070,-.469,-.022,.4884,.5069,.25),
					(-.637,0,0,.501,.8562,.2513,.1)
	]
	
	IFS_TREE2 = [
					 (0.000,0.000,0.000,0.600,0.00,-0.065,0.100),
					 (0.440,0.000,0.000,0.550,0.00,0.200,0.180),
					 (0.343,-0.248,0.199,0.429,-0.03,0.100,0.180),
					 (0.343,0.248,-0.199,0.429,0.03,0.100,0.180),
					 (0.280,-0.350,0.280,0.350,-0.05,0.000,0.180),
					 (0.280,0.350,-0.280,0.350,0.05,0.000,0.180)
	]
	
	IFS_WREATH = [
					(0.475,-0.823,0.823,0.475,1.0,1.0,0.8),
					(0.5,0.5,0.0,0.5,0.5,0.0,0.2),
	]
	
	#    IFS = IFS_generate()

	IFSs = [ IFS_HeighwayDragon, IFS_BarnsleyFern, IFS_1, IFS_ANCHORS, 
			 IFS_ANGLES,IFS_BABYLON,IFS_CASTLE,IFS_CLOUD, IFS_CORAL, IFS_CORAL1,
			 IFS_COSMOS, IFS_CRYSTAL, IFS_CRYSTAL4, IFS_CURL, IFS_DOGS, IFS_DRAGON1, IFS_DRAGON2,
			 IFS_FERN1, IFS_FLOOR, IFS_FLOOR1,IFS_FLOOR2,IFS_FLYFISH, IFS_LEAF, IFS_LEAF2,
			 IFS_POSIES2, IFS_SATDISH, IFS_SPIRAL, IFS_SPIRAL1, IFS_SPIRAL2,IFS_SPIRAL3,
			 IFS_STICKS,IFS_SWIRL,IFS_TOWER,IFS_TREE,IFS_TREE1,IFS_TREE2,IFS_WREATH
			 
			 
			 ] #, IFS_RAND]

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