# @abrightmoore
from numpy import *
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys


from PIL import Image, ImageDraw



def createImage(width,height):
	formulaR,formulaG,formulaB = getFormulas()
	return createImgWithRules(width,height,formulaR,formulaG,formulaB)

def createImgWithRules(width,height,formulaR,formulaG,formulaB):

	img = Image.new('RGBA', size=(width, height), color=(128, 100, 64))
	# Choose what type of image to create
	chance = random()
	if chance < 0.03:
		print "Making squiggly lines"
		img = InkSplodgyWiggleLinesCol(img)
	elif chance < 0.06:
		print "Making an InkSplodgyLineSpiralWiggleLines"
		InkSplodgyLineSpiralWiggleLines(img)
	elif chance < 0.09:
		print "Making a InkSplodgyWiggleLines"		
		InkSplodgyWiggleLines(img)
	elif chance < 0.12:
		print "InkSplodgyLineSpiralWiggle"
		InkSplodgyLineSpiralWiggle(img)
	elif chance < 0.15:
		print "InkSplodgyLineSpiral"		
		InkSplodgyLineSpiral(img)
	elif chance < 0.18:
		print "InkSplodgy"		
		InkSplodgy(img)
	elif chance < 0.25:
		print "Making a SquaresInk"
		SquaresInk(img)
	elif chance < 0.35:
		print "Making a ColourSwatch"
		makeColourSwatch(img)
	elif chance < 0.55:
		print "Making an InterferenceImage"
		makeInterferenceImage(img)
	elif chance < 0.65:
		print "Making a TrigImage with spheres"
		makeTrigImage(img,formulaR,formulaG,formulaB)
		pix = img.load()
		# Spheres
		for i in xrange(0,15):
			f1,f2,f3 = getFormulas()
			radius = randint(abs(width>>8),abs(width>>2)+1)
			maxPx = width-radius-1
			maxPy = height-radius-1
			count = 100
			while count > 0 and (maxPx < radius or maxPy < radius): # Regenerate on bad numbers
				count = count -1
				radius = randint(width>>8,width>>1)
				maxPx = width-radius-1
				maxPy = height-radius-1
			px = randint(radius,width-radius-1)
			py = randint(radius,height-radius-1)
			drawTrigSphere(pix,px,py,radius,f1,f2,f3)
	elif chance < 0.85:
		print "Making a TrigImage"
		makeTrigImage(img,formulaR,formulaG,formulaB)
	elif chance < 0.98:
		print "Making a blendedImage"
		ox,oy,sx,sy = (-2.0,-1.5,3.0,3.0)
#               ox,oy,sx,sy = (-1.108,-0.230,0.005,0.005)
		methods = ["Circle","Spike","Blend","Spike","Blend","Spike","Blend","Spike","Blend","Spike","Blend"]
		imgArray = []
		for i in xrange(0,5): # This section finds a deep layer in the Mandelbrot
			(new_ox,new_oy,new_sx,new_sy) = drawMandelbrot(img,ox,oy,sx,sy)
			# filename = "AJTrimage_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+formulaR+"_"+formulaG+"_"+formulaB+".png"
			# img.save(filename)

			#newimg.save("AJFractrigimage_"+str(randint(111111111,999999999))+".png")
			ox = new_ox
			oy = new_oy
			sx = new_sx
			sy = new_sy
			imgArray.append(img)
		if len(imgArray) > 1:
			img = imgArray[randint(1,len(imgArray)-1)] # Choose one of the images generated

			trigImg = Image.new('RGBA', size=(width, height), color=(0, 0, 0))
			(formulaR,formulaG,formulaB) = getFormulas()
			makeTrigImage(trigImg,formulaR,formulaG,formulaB)
			#trigImg.save("AJFractrigMooshyimage_"+str(randint(111111111,999999999))+".png")

			img = mergeImages(img,trigImg, methods[randint(0,len(methods)-1)])
			
			if random() < 0.3:
				writingImg = InkSplodgyWiggleLinesCol(img)
				img = mergeImages(writingImg,img, "Spike" )
		else:
			return imgArray[0]
		# for imgA in imgArray:
			# filename = "AJMandelbrot_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+str(randint(111111111,999999999))+".png"
			# imgA.save(filename)
	else: # A curvy graph
		print "Making a TrigFuncGraphImage"
		makeTrigFuncGraphImage(img,formulaR,formulaG,formulaB)
	# img.save("Testimage"+str(randint(111111111,999999999))+".png")
	# collapseAlpha(img)
	return img

def createNoiseImage(img):
	width = img.size[0]
	height = img.size[1]

#        C = getComplementaryColours(randint(3,128))
	C = []
	if randint(1,5) < 4:
		C = getRandomAnalogousColours()
	else:
		C = getRandomComplementaryColours()

	p = img.load()
	z = randint(0,1000000000)
	for y in xrange(0,width):
		for x in xrange(0,width):
			n = noise(x,y,z)
			p[x,y] = C[int(abs(float(n*len(C))))%len(C)]
			
def createImgFile(width,height,author): # DEPRECATED
	# In memory file method used is by Rolo http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
	FILENAMEIMAGE = '@abrightmoore_@TrigonometryBot_output.png'

	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))

	# Choose what type of image to create
	chance = random()
	if chance < 1.0:
		img = InkSplodgyWiggleLinesCol(img)
	elif chance < 0.05:
		makeTrigImage(img,formulaR,formulaG,formulaB)
		pix = img.load()
		# Spheres
		for i in xrange(0,15):
			f1,f2,f3 = getFormulas()
			radius = randint(width>>8,width>>1)
			px = randint(radius,width-radius-1)
			py = randint(radius,height-radius-1)
			drawTrigSphere(pix,px,py,radius,f1,f2,f3)
	elif chance < 0.055: # A curvy graph
		makeTrigFuncGraphImage(img,formulaR,formulaG,formulaB)
	elif chance < 0.1:
		makeColourSwatch(img)
	elif chance < 0.2:
		makeInterferenceImage(img)
	elif chance < 0.7:
		ox,oy,sx,sy = (-2.0,-1.5,3.0,3.0) # Mandelbrot
		imgArray = []
		for i in xrange(0,randint(1,8)):
			(new_ox,new_oy,new_sx,new_sy) = drawMandelbrot(img,ox,oy,sx,sy)
			imgArray.append(img)
			img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))
#			filename = "AJTrimage_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+formulaR+"_"+formulaG+"_"+formulaB+".png"
#			img.save(filename)
			ox = new_ox
			oy = new_oy
			sx = new_sx
			sy = new_sy
		if len(imgArray) > 0:
			img = imgArray[randint(1,len(imgArray)-1)] # Choose one of the images generated
#		for imgA in imgArray:
#			filename = "AJMandelbrot_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+str(randint(111111111,999999999))+".png"
#			imgA.save(filename)
	else:
		(formulaR,formulaG,formulaB) = getFormulas()
		makeTrigImage(img,formulaR,formulaG,formulaB)
		memoryAppend((formulaR,formulaG,formulaB,author))
	
#	if PREVIMG != None and random() > 0.8:
#		blend(img,PREVIMG)
#	PREVIMG = img
		
	file = BytesIO()	
	img.save(file, 'png')
	file.name = FILENAMEIMAGE
	file.seek(0)
	return file # Twitter works with files 
	
def mergeImages(img1,img2,strategy):
	# Assumes both images are the same dimensions
	width = img1.size[0]
	height = img1.size[1]
	width2 = img2.size[0]
	height2 = img2.size[1]
	gapx = (width-width2)>>1
	gapy = (height-height2)>>1
	cw = width >>1
	ch = height >>1
	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))
	pix = img.load()
	pix1 = img1.load()
	pix2 = img2.load()
	radius = (width+height)>>2
	rad2 = radius**2
	if strategy == "Circle":
		for x in xrange(0,width):
			dx = cw - x
			distx = dx**2
			for y in xrange(0,height):
				dy = ch - y
				dist = distx + dy**2
				if dist > rad2:
						pix[x,y] = pix2[x,y]
				else: # blend
					(r1,g1,b1,a1) = pix1[x,y]
					(r2,g2,b2,a2) = pix2[x,y]
					ratio = cos(abs(float(dist)/float(rad2)*pi/2))
					# print ratio
					ratioInv = 1.0-ratio
					(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
					if r > 255:
						r = 255
					if g > 255:
						g = 255
					if b > 255:
						b = 255
					pix[x,y] = (int(r),int(g),int(b),int(a))
	if strategy == "Spike":
		for x in xrange(0,width):
			dx = cw - x
			distx = dx**2
			for y in xrange(0,height):
				dy = ch - y
				dist = distx + dy**2
				if dist > rad2:
					pix[x,y] = pix2[(x-gapx)%width2,(y-gapy)%height2]
				else: # blend
					(r1,g1,b1,a1) = pix1[x,y]
					(r2,g2,b2,a2) = pix2[(x-gapx)%width2,(y-gapy)%height2]
					ratio = 1.0-sin(abs(float(dist)/float(rad2)*pi/2))
					# print ratio
					ratioInv = 1.0-ratio
					(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
					if r > 255:
						r = 255
					if g > 255:
						g = 255
					if b > 255:
						b = 255
					pix[x,y] = (int(r),int(g),int(b),int(a))
	if strategy == "Blend":
		for x in xrange(0,width):
			for y in xrange(0,height):
				(r1,g1,b1,a1) = pix1[x,y]
				(r2,g2,b2,a2) = pix2[x,y]
				ratio = 0.5
				ratioInv = 1.0-ratio
				(r,g,b,a) = (ratio*r1+ratioInv*r2,ratio*g1+ratioInv*g2,ratio*b1+ratioInv*b2,255)
				if r > 255:
					r = 255
				if g > 255:
					g = 255
				if b > 255:
					b = 255
				pix[x,y] = (int(r),int(g),int(b),int(a))                                        
	return img                                        

def drawMandelbrot(img,ox,oy,sx,sy):
	width = img.size[0]
	height = img.size[1]
	img.paste( (0,0,0), [0,0,width,height])
        MAXITER = 256
        coloursArray = [[(0.0,0,7,100),(0.16,32,107,203),(0.42,237,255,255),(0.6425,255,170,0),(0.8575,0,2,0),(1.0,30,0,0)], # after NightElfik
                        [(0.0,0,randint(10,100),randint(10,100)),(0.16,randint(10,100),randint(10,107),randint(10,203)),(0.42,randint(10,235),randint(10,255),randint(10,255)),(0.6425,randint(10,255),randint(10,170),0),(0.8575,0,2,0),(1.0,30,0,0)],
						[(0.0,0,randint(128,255),randint(128,255)),(0.16,randint(128,255),randint(128,255),randint(128,256)),(0.42,randint(128,255),randint(128,255),randint(128,255)),(0.6425,randint(128,255),randint(128,255),0),(0.8575,0,2,0),(1.0,30,0,0)],
						
                        ]
        colours = coloursArray[randint(0,len(coloursArray)-1)]              
        # Window on the number plane

        qx = sx/float(width) # Quantum of distance
        qy = sy/float(height) # Quantum of distance

        nextP = (-1.0,0.0)
        pixels = img.load()
        for x in xrange(0,width):
                for y in xrange(0,height):
                        px = ox+qx*x # real 
                        py = oy+qy*y # imaginary
                        # print px,py
                        count = MAXITER
                        dist2 = px**2+py**2
                        cx = px
                        cy = py
                        while count >=0 and dist2 < 4:
                                count = count-1
                                x_new = cx**2 - cy**2 + px
                                cy = 2*cx*cy + py
                                cx = x_new
                                dist2 = cx**2 + cy**2
                        if count > 0:
                                posn = float(count)/float(MAXITER)
                                (p1, r1, g1, b1) = colours[0]
                                for (p2, r2, g2, b2) in colours:
                                        if p1 <= posn and posn < p2:
                                                posnDelta = posn - p1
                                                gap = p2 - p1
                                                colPos = posnDelta/gap
                                                
                                                pixels[x,y] = (int(r1+colPos*(r2-r1))%256,
                                                                      int(g1+colPos*(g2-g1))%256,
                                                                      int(b1+colPos*(b2-b1))%256,255)
#                                               if count < 10 and random() < 0.5: # and count < MAXITER-MAXITER>>2: choose a zoom
#                                                        nextP = (px,py)
#                                                        print nextP
                                                exit
                                        (p1, r1, g1, b1) = (p2, r2, g2, b2)

                        else:
                                pixels[x,y] = (0,0,80,255)
        # Work out where to go next
        diffImg = avgDifference(img)
        zoomCol = (255,255,0,255)
        zoomRadius = randint(10,width>>2)
        pixDiff = diffImg.load()
        P = []
        for x in xrange(0,width-2):
                for y in xrange(0,height-2):
                        (r,g,b,a) = pixDiff[x,y]
                        if r > 32 and random() < 0.01: # Threshhold for finding interesting edges
                                pixDiff[x,y] = (255,0,0,255)
                                P.append((x,y))
        # diffImg.save("Diff"+str(randint(111111111,999999999))+".png")
        if len(P) > 0:
                (x,y) = P[randint(0,len(P)-1)]
                px = ox+qx*x
                py = oy+qy*y
                for ix in xrange(x-zoomRadius,x+zoomRadius):
                        if ix >0 and ix < width-1:
                                if y-zoomRadius > 0:
                                        pixDiff[ix-1,y-zoomRadius-1] = zoomCol                                              
                                if y+zoomRadius < height-1:
                                        pixDiff[ix-1,y+zoomRadius-1] = zoomCol
                for iy in xrange(y-zoomRadius,y+zoomRadius):
                        if iy >0 and iy < height-1:
                                if x-zoomRadius > 0:
                                        pixDiff[x-zoomRadius-1,iy-1] = zoomCol                                              
                                if x+zoomRadius < width-1:
                                        pixDiff[x+zoomRadius-1,iy-1] = zoomCol
                                                
                # diffImg.save("Diff"+str(randint(111111111,999999999))+".png")
                return (px-zoomRadius*qx,py-zoomRadius*qx,zoomRadius*2*qx,zoomRadius*2*qy)
        else:
                return (-2.0,-1.5,3.0,3.0) # Top level again, couldn't find a point to play with
                
def avgDifference(img):
	width = img.size[0]
	height = img.size[1]
	pix = img.load()
	imgB = Image.new('RGBA', size=(width-2, height-2), color=(0, 0, 0))
	pixB = imgB.load()
        for x in xrange(1,width-1):
                for y in xrange(1,height-1):
                        avgDelta = 0
                        (vr,vg,vb,va) = pix[x,y]
                        for dx in xrange(-1,2):
                                for dy in xrange(-1,2):
                                        if not (dx == 0 and dy == 0):
                                                (nr,ng,nb,na) = pix[x+dx,y+dy]
                                                avgDelta = avgDelta + int(abs(vr+vg+vb-(nr+ng+nb))/3)
                        avgDelta = int(avgDelta / 8)
                        pixB[x-1,y-1] = (avgDelta,avgDelta,avgDelta,255)
        return imgB

def makeTrigImage(img,formulaR,formulaG,formulaB): # A kind of psychedelic picture based on application of formula across each location on a place.
	width = img.size[0]
	height = img.size[1]

	a = 255
	cw = width>>1
	ch = height>>1
	scale = 0

	scaleDelta = 1
	if False:
		scaleDelta = -randint(1,(width+height)>>3)
		if R.random() > 0.5:
			scaleDelta = -scaleDelta
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = (2.0*pi)/float(height*scaleDelta)

	pixels = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			px = QUANTUMX * float(x-cw)
			py = QUANTUMY * float(y-ch)
		
			r = calcFormula(formulaR,px,py)*127+127
			# print r
			g = calcFormula(formulaG,px,py)*127+127
			b = calcFormula(formulaB,px,py)*127+127
			if r > 255:
				r = 255
			elif r < 0:
				r = 0
			if g > 255:
				g = 255
			elif g < 0:
				g = 0                                           
			if b > 255:
				b = 255
			elif b < 0:
				b = 0                                           

			pixels[int(x),int(y)] = (int(r),int(g),int(b),int(a))
	
def blend(imgA,imgB):
	width = imgA.size[0]
	height = imgA.size[1]
	pixA = imgA.load()
	pixB = imgB.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			(rA,gA,bA,aA) = pixA[x,y]
			(rB,gB,bB,aB) = pixB[x,y]
			pixA = (rA>>1+rB>>1,gA>>1+gB>>1,bA>>1+bB>>1,aA>>1+aB>>1)

def createImgFileWithRules(width,height,ruleRed,ruleGreen,ruleBlue,author):
	# In memory file method used is by Rolo http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
	FILENAMEIMAGE = '@abrightmoore_@TrigonometryBot_output.png'
	
	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))

	# Choose what type of image to create
	if True:
		(formulaR,formulaG,formulaB) = (ruleRed,ruleGreen,ruleBlue)
		makeTrigImage(img,formulaR,formulaG,formulaB)
		memoryAppend((formulaR,formulaG,formulaB,author))

	file = BytesIO()	
	img.save(file, 'png')
	file.name = this.FILENAMEIMAGE
	file.seek(0)
	return file # Twitter works with files 

def drawGraph(img,col):
	width = img.size[0]
	height = img.size[1]
	img.paste( (192,192,200), [0,0,width,height])

	a = 255
	cw = width >> 1
	ch = height >> 1
	scale = 1
	scaleDelta = 1
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = (2.0*pi)/float(height*scaleDelta)        
	pixels = img.load()
 
	for x in xrange(0,width):
		pixels[x,ch] = col
	for y in xrange(0,height):
		pixels[cw,y] = col
	del pixels

def makeInterferenceImage(img):
	width = img.size[0]
	height = img.size[1]
	P = []
        numPoints = randint(1,17)
        theRange = (width+height) ** 2
        
        for i in xrange(0,numPoints):
                scale = randint(8,1280)
                P.append((random()*pi*2.0,randint(0,theRange),random(),random()*scale))
                if random() < 0.2:
                        P.append((random()*pi*2.0,randint(0,width>>2),random(),random()*scale)) 
#        C = getComplementaryColours(randint(3,128))
		C = []
		if randint(1,5) < 4:
			C = getRandomAnalogousColours()
		else:
			C = getRandomComplementaryColours()

        # render the image
	pixels = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
                        contribution = 0.0
                        for (ang,dist,amp,wavelength) in P:
                                ox = dist*cos(ang)
                                oy = dist*sin(ang)
                                dx = ox - x
                                dy = oy - y
                                d = sqrt(dx**2+dy**2)
                                contribution = contribution + amp*cos(d/wavelength)
                        size = contribution*float(len(C))
                        #print size
                        pixels[x,y] = C[int(abs(float(size)))%len(C)]


def makeTrigFuncGraphImage(img,formulaR,formulaG,formulaB): # A 2D height graph
	width = img.size[0]
	height = img.size[1]
 #       img.fill((127,127,127,255))

	a = 255
	cw = width >> 1
	ch = height >> 1
	scale = 1
	scaleDelta = 1
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = float(height*scaleDelta)/256.0       

	drawGraph(img,(250,250,250,255))
	pixels = img.load()
	draw = ImageDraw.Draw(img)        

	prevR = None
	prevG = None
	prevB = None
	
	for x in xrange(0,width):
		px = QUANTUMX * float(x-cw)
		r = calcFormula(formulaR,px,0)*127+127
		g = calcFormula(formulaG,px,0)*127+127
		b = calcFormula(formulaB,px,0)*127+127
		if r > 255:
			r = 255
		elif r < 0:
			r = 0
		if g > 255:
			g = 255
		elif g < 0:
			g = 0                                           
		if b > 255:
			b = 255
		elif b < 0:
			b = 0                                           
		pyr = height-QUANTUMY * r-1      
		if pyr >= 0 and pyr < height:
			pixels[int(x),int(pyr)] = (int(r),0,0,int(a))
		pyg = height-QUANTUMY * g-1     
		if pyg >= 0 and pyg < height:
			pixels[int(x),int(pyg)] = (0,int(g),0,int(a))
		pyb = height - QUANTUMY * b-1      
		if pyb >= 0 and pyb < height:
			pixels[int(x),int(pyb)] = (0,0,int(b),int(a))
		if prevR != None: draw.line(prevR+(x,int(pyr)), (int(r),0,0,int(a)))
		if prevG != None: draw.line(prevG+(x,int(pyg)), (0,int(g),0,int(a)))
		if prevB != None: draw.line(prevB+(x,int(pyb)), (0,0,int(b),int(a)))

		prevR = (x,int(pyr))
		prevG = (x,int(pyg))
		prevB = (x,int(pyb))
	del draw
	del pixels


def drawTinyTrigSphere(pix,px,py,radius,f1,f2,f3):

	r2 = radius**2
	scaleDelta = 1.0
	QUANTUMX = (2.0*pi)/float(radius*scaleDelta)
	QUANTUMY = (2.0*pi)/float(radius*scaleDelta)
	for x in xrange(-radius,radius):
		dx = x**2
		# ppx = x+px
		ppx = QUANTUMX * float(x)
		for y in xrange(-radius,radius):
			
			ppy = QUANTUMY * float(y)
		
			dy = y**2
			# ppy = y+py
			if (dx+dy) < r2:
				r = calcFormula(f1,ppx,ppy)*127+127
				g = calcFormula(f2,ppx,ppy)*127+127
				b = calcFormula(f3,ppx,ppy)*127+127

				if r > 255:
					r = 255
				elif r < 0:
					r = 0
				if g > 255:
					g = 255
				elif g < 0:
					g = 0                                           
				if b > 255:
					b = 255
				elif b < 0:
					b = 0                                           

				
				pix[px+x,py+y] = (int(r),int(g),int(b),255)

def makeColourSwatch(img):
	width = img.size[0]
	height = img.size[1]

	a = 255
	cw = width>>1
	ch = height>>1
	scale = 0

	scaleDelta = 1
	QUANTUMX = (2.0*pi)/float(width*scaleDelta)
	QUANTUMY = (2.0*pi)/float(height*scaleDelta)

	C = []
	if randint(1,5) < 4:
		C = getRandomAnalogousColours()
	else:
		C = getRandomComplementaryColours()
		
	for j in xrange(0,3):
                Clen = len(C)
                for i in xrange(0,Clen):
                        (r,g,b) = (C[i])
                        C.append((r>>1,g>>1,b>>1)) # Add Half intensity colours.
	if random() > 0.5:
		C.append((255,255,255))
	if random() > 0.5:
		C.append((0,0,0))
						
	pixels = img.load()
	bands = width/len(C)+1
	print bands
	for x in xrange(0,width):
		for y in xrange(0,height):
			pixels[x,y] = C[int((x+y)/int(bands))%len(C)]
			

				
def drawTrigSphere(pix,px,py,radius,f1,f2,f3):

	r2 = radius**2
	scaleDelta = 1.0
	QUANTUMX = (2.0*pi)/float(radius*scaleDelta)
	QUANTUMY = (2.0*pi)/float(radius*scaleDelta)
	for x in xrange(-radius,radius):
		dx = x**2
		# ppx = x+px
		ppx = QUANTUMX * float(x)
		for y in xrange(-radius,radius):
			
			ppy = QUANTUMY * float(y)
		
			dy = y**2
			# ppy = y+py
			if (dx+dy) < r2:
				r = calcFormula(f1,ppx,ppy)*127+127
				g = calcFormula(f2,ppx,ppy)*127+127
				b = calcFormula(f3,ppx,ppy)*127+127

				if r > 255:
					r = 255
				elif r < 0:
					r = 0
				if g > 255:
					g = 255
				elif g < 0:
					g = 0                                           
				if b > 255:
					b = 255
				elif b < 0:
					b = 0                                           

				
				pix[px+x,py+y] = (int(r),int(g),int(b),255)        

def RotatePoint((x,y,z), (cx,cy,cz), theta, phi): # rotate around an arbitrary origin
	# Plot the new point
	dx = x - cx
	dy = y - cy
	d = sqrt(dy**2 + dx**2)
	t = atan2(dy, dx) # tilt around the z axis
	(px,py,pz) = ( cos(t+phi)*d, sin(t+phi)*d, z ) # tilt offset around the z axis
	dz = pz - cz
	dx = px - cx
	d = sqrt(dz**2 + dx**2)
	t = atan2(dz, dx) # tilt around the y axis
	return ( cos(t+theta)*d, py, sin(t+theta)*d ) # tilt offset around the z axis

def UnRotatePoint((x,y,z), (cx,cy,cz), theta, phi): # rotate around an arbitrary origin. Order of operations reversed
	# Plot the new point
	dz = z - cz
	dx = x - cx
	d = sqrt(dz**2 + dx**2)
	t = atan2(dz, dx) # tilt around the y axis
	(px,py,pz) =( cos(t-theta)*d, y, sin(t-theta)*d ) # tilt offset around the z axis

	dx = px - cx
	dy = py - cy
	d = sqrt(dy**2 + dx**2)
	t = atan2(dy, dx) # tilt around the z axis
	return ( cos(t-phi)*d, sin(t-phi)*d, pz ) # tilt offset around the z axis

def getComplementaryColours(quantity):
	COLMASK = 0xff
	result = []

#       COLBASE = 0.3
	# 0.3 so we don't make it too dark nor light
#       r = (COLBASE+random()/2)*256 # x
#       g = (COLBASE+random()/2)*256 # y
#       b = (COLBASE+random()/2)*256 # z

	r = randint(32,255)
	g = randint(32,255)
	b = randint(32,255)

	result.append((r,g,b))

	# This gives a colour in the RGB colour cube. Find out what angles these are
	disth2 = r**2+g**2
	theta = atan2(r,g)
	phi = atan2(b,sqrt(disth2))
	# - to find the other two colours, we need to rotate this point around the line from 0,0,0 to 1,1,1 by the right number of degrees and read off the coordinates
	angleRot = pi*2.0/float(quantity)
	# rotate up 45 degrees and back 45 degrees
	angleDelta = pi/4

	(x,y,z) = RotatePoint((r,g,b), (0,0,0), -angleDelta, angleDelta) # Shift the axis to normalise space along r=g=b line
#       print (x,y,z)

	for i in xrange(1,quantity):
		(r1,g1,b1) = RotatePoint((x,y,z), (0,0,0), -angleDelta*i, 0) # find each rotation in normalised space
		result.append(UnRotatePoint((r1,g1,b1),(0,0,0),-angleDelta,angleDelta)) # Map back to the colour cube

	resultConstrained = []
	for (r,g,b) in result:
#               if r > 255 or g > 255 or b > 255:
#                       print r,g,b
		if r > 255:
			r = 255
		if g > 255:
			g = 255
		if b > 255:
			b = 255
		if r < 0:
			r = 0
		if g < 0:
			g = 0
		if b < 0:
			b = 0
		resultConstrained.append((int(r)&COLMASK,int(g)&COLMASK,int(b)&COLMASK))

	return resultConstrained

	
def getRandomComplementaryColours():
	return getComplementaryColours(randint(2,64))

def getRandomAnalogousColours():
	C = getComplementaryColours(12)
	R = []
	for i in xrange(0,2):
		R.append(C[i])
	return R

	
def getFormulas():
	formulaR = makeRandomFormula()
	formulaG = makeRandomFormula()
	formulaB = makeRandomFormula()
	return (formulaR,formulaG,formulaB)

def makeRandomFormula():
	result = ""
	funcs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRS"
	iters = randint(1,11)
	for i in xrange(0,iters):
		result=result+(funcs[randint(0,len(funcs)-1)])
	return result
	
def calcFormula(formula,x,y):
	# parse formula, substitute parameters, adjust result
	val = 1.0
	err = 0
	for c in formula:
		if c == "a":
			val = val* sin(y)
		elif c == "b":
			val = val* cos(y)
		elif c == "c":
			try:
				val = val* tan(y)
			except:
				err = err+1
		elif c == "d":
			val = val* sin(x)
		elif c == "e":
			val = val* cos(x)
		elif c == "f":
			try:
				val = val* tan(x)
			except:
				err = err+1
		elif c == "g":
			val = val* sin(x+y)
		elif c == "h":
			val = val* cos(x+y)
		elif c == "i":
			try:
				val = val* tan(x+y)
			except:
				err = err+1
		elif c == "j":
			val = val* sin(x-y)
		elif c == "k":
			val = val* cos(x-y)
		elif c == "l":
			try:
				val = val* tan(x-y)
			except:
				err = err+1
		elif c == "m":
			if y != 0:
				val = val* x/y
		elif c == "n":
			if x != 0:
				val = val* y/x
		elif c == "o":
			val = val* (x-y)
		elif c == "p":
			val = val* (x+y)
		elif c == "q":
			val = val* x*y
		elif c == "r":
			val = val* atan2(y,x)
		elif c == "s":
			val = val* x**2 
		elif c == "t":
			val = val* x**3 
		elif c == "u":
			try:
				val = val* asin(x)
			except:
				err = err+1
		elif c == "v":
			try:
				val = val* acos(x)
			except:
				err = err+1
		elif c == "w":
			try:
				val = val* atan(x)
			except:
				err = err+1
		elif c == "x":
			try:
				val = val* hypot(x,y)
			except:
				err = err+1
		elif c == "y":
			try:
				val = val* acosh(x)
			except:
				err = err+1
		elif c == "z":
			try:
				val = val* asinh(x)
			except:
				err = err+1
		elif c == "A":
			try:
				val = val* atanh(x)
			except:
				err = err+1
		elif c == "B":
			try:
				val = val* cosh(x)
			except:
				err = err+1
		elif c == "C":
			try:
				val = val* sinh(x)
			except:
				err = err+1
		elif c == "D":
			try:
				val = val* tanh(x)
			except:
				err = err+1
		elif c == "E":
			val = val* min(x,y)
		elif c == "F":
			val = val* max(x,y)

		elif c == "G":
			val = val* sin(val)
		elif c == "H":
			val = val* cos(val)
		elif c == "I":
			try:
				val = val* tan(val)
			except:
				err = err+1
		elif c == "J":
			val = val**2
		elif c == "K":
			try:
				val = val* asin(val)
			except:
				err = err+1
		elif c == "L":
			try:
				val = val* acos(val)
			except:
				err = err+1
		elif c == "M":
			try:
				val = val* atan(val)
			except:
				err = err+1
		elif c == "N":
			try:
				val = val* acosh(val)
			except:
				err = err+1
		elif c == "O":
			try:
				val = val* asinh(val)
			except:
				err = err+1
		elif c == "P":
			try:
				val = val* atanh(val)
			except:
				err = err+1
		elif c == "Q":
			try:
				val = val* cosh(x)
			except:
				err = err+1
		elif c == "R":
			try:
				val = val* sinh(val)
			except:
				err = err+1
		elif c == "S":
			try:
				val = val* tanh(val)
			except:
				err = err+1
			
	return val

# Older code lifted from the prototype stage - @abrightmoore
	
def adjustByOneRandomly(R,x,l,u):
	x = x+R.randint(-1,1)
	if x > u:
		x = u
	if x < l:
		x = l
	return x

def adjustColourRandomly(R,r,g,b,l,u):
	x = R.randint(-1,1)
	r = r+x
	g = g+x
	b = b+x
	if r > u:
		r = u
	elif r < l:
		r = l
	if g > u:
		g = u
	elif g < l:
		g = l
	if b > u:
		b = u
	elif b < l:
		b = l
	return (r,g,b)

def fill(pixels,width,height,r,g,b,a):
	for x in xrange(0,width):
		for y in xrange(0,height):
			pixels[x,y] = (r,g,b,a)

def setAlpha(pixels,width,height,a):
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a0) = pixels[x,y]
			pixels[x,y] = (r,g,b,a)
			
def example_SquaresSquared(RAND): # Reference
	(R,SEED) = RAND
	SMOOTHAMOUNT = 4
	width = 1400
	height = width
	maxRadius = R.randint(1,4) # int(width/20)
	border = 3*maxRadius
	(filename,width,height) = ("ajb_example_SquaresSquared_"+str(SEED)+"_"+str(randint(10000000,99999999)),width,height)
	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	(r,g,b,a) = (207,157,51,0)
	fill(pixels,width,height,r,g,b,a)
	
	for ii in xrange(1,4):
		charSizeW = R.randint(4,int(width/2))
		charSizeH = charSizeW
	
		# Navigate the canvas
		posY = 0
		radius = maxRadius
	#	(r,g,b,a) = (R.randint(0,255),R.randint(0,255),R.randint(0,255),255)

		spread = R.randint(50,100)*0.01
		#(r,g,b,a) = (124,85,79,16)	
		rr = R.randint(1,128)
		(r,g,b,a) = (int(rr*2/3),rr,rr,R.randint(8,16))	
		
		while posY < height:
			posX = 0

			while posX < width:
				if R.random() < spread:
					#(r,g,b,a) = (R.randint(0,255),R.randint(0,255),R.randint(0,255),128)
					(r,g,b,a) = (int(rr*2/3),rr,rr,R.randint(8,16))		
				# For each square
				for e in xrange(0,int(charSizeW)/(ii*2)):
					d = e
					
					for x in xrange(posX,posX+charSizeW):
						
						y = posY+d
						try:
							drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
						except:
							print "oops!"
						(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)

						y = posY+charSizeH-1-d
						try:
							drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
						except:
							print "oops!"
						(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)

					for y in xrange(posY,posY+charSizeH):

						x = posX+d
						try:
							drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
						except:
							print "oops!"
						(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)
						x = posX+charSizeW-1-d
						try:
							drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
						except:
							print "oops!"
						(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)
			
				posX = posX+charSizeW		
			posY = posY+charSizeH			
	setAlpha(pixels,width,height,255)
	img.save(filename+".png")
	invertPixelsNotAlpha(img)
	img.save(filename+"_i.png")
	print filename
	print "Complete"

			
def example_Squares(RAND): # Reference
	(R,SEED) = RAND
	SMOOTHAMOUNT = 4
	width = 1400
	height = width
	maxRadius = R.randint(1,4) # int(width/20)
	border = 3*maxRadius
	(filename,width,height) = ("ajb_example_Squares_"+str(SEED)+"_"+str(randint(10000000,99999999)),width,height)
	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	charSizeW = R.randint(4,int(width/2))
	charSizeH = charSizeW
	
	# Navigate the canvas
	posY = 0
	radius = maxRadius
#	(r,g,b,a) = (R.randint(0,255),R.randint(0,255),R.randint(0,255),255)
	(r,g,b,a) = (207,157,51,128)
	fill(pixels,width,height,r,g,b,a)
	spread = R.randint(50,100)*0.01
	(r,g,b,a) = (124,85,79,64)	
	while posY < height:
		posX = 0

		while posX < width:
			if R.random() < spread:
				(r,g,b,a) = (R.randint(0,255),R.randint(0,255),R.randint(0,255),128)
				(r,g,b,a) = (124,85,79,64)	
			# For each square
			for e in xrange(0,int(charSizeW)/4):
				d = e*2
				
				for x in xrange(posX,posX+charSizeW):
					
					y = posY+d
					try:
						drawPixel(pixels,r,g,b,a,x,y)
					except:
						print "oops!"
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)

					y = posY+charSizeH-1-d
					try:
						drawPixel(pixels,r,g,b,a,x,y)
					except:
						print "oops!"
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)

				for y in xrange(posY,posY+charSizeH):

					x = posX+d
					try:
						drawPixel(pixels,r,g,b,a,x,y)
					except:
						print "oops!"
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)
					x = posX+charSizeW-1-d
					try:
						drawPixel(pixels,r,g,b,a,x,y)
					except:
						print "oops!"
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)
		
			posX = posX+charSizeW		
		posY = posY+charSizeH			
	img.save(filename+".png")
	invertPixelsNotAlpha(img)
	img.save(filename+"_i.png")
	print filename
	print "Complete"
			
def SquaresInk(img): # Reference
	width = img.size[0]
	height = img.size[1]

	error = 0
	R = Random()
	SMOOTHAMOUNT = 4
	maxRadius = R.randint(1,4) # int(width/20)
	border = 3*maxRadius
	#(filename,width,height) = ("ajb_example_SquaresInk_"+str(SEED)+"_"+str(randint(10000000,99999999)),width,height)
	#img = Image.new('RGBA', (width, height))
	pixels = img.load()
	charSizeW = R.randint(4,128)
	charSizeH = charSizeW
	
	# Navigate the canvas
	posY = 0
	radius = maxRadius
#	(r,g,b,a) = (R.randint(0,255),R.randint(0,255),R.randint(0,255),255)
	(r,g,b,a) = (207,157,51,128)
	fill(pixels,width,height,r,g,b,a)
	spread = R.randint(50,100)*0.01
	(r,g,b,a) = (124,85,79,64)	
	while posY < height:
		posX = 0

		while posX < width:
			if R.random() < spread:
				(r,g,b,a) = (R.randint(0,255),R.randint(0,255),R.randint(0,255),128)
				(r,g,b,a) = (124,85,79,64)	
			# For each square
			for e in xrange(0,int(charSizeW)/4):
				d = e*2
				
				for x in xrange(posX,posX+charSizeW):
					
					y = posY+d
					drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)

					y = posY+charSizeH-1-d
					drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)

				for y in xrange(posY,posY+charSizeH):

					x = posX+d
					drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)
					x = posX+charSizeW-1-d
					drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y)
					(r,g,b) = adjustColourRandomly(R,r,g,b,0,255)
		
			posX = posX+charSizeW		
		posY = posY+charSizeH			
	#img.save(filename+".png")
	invertPixelsNotAlpha(img)
	#img.save(filename+"_i.png")
	#print filename
	#print "Complete"
	return img
		
def InkSplodgyWiggleLinesCol(img): # Reference
	width = img.size[0]
	height = img.size[1]

	error = 0
	R = Random()
	SMOOTHAMOUNT = 4
	maxRadius = R.randint(1,4) # int(width/20)
	border = 3*maxRadius
	# (filename,width,height) = ("ajb_example_InkSplodgyWiggleLinesCol_"+str(SEED)+"_"+str(randint(10000000,99999999))+".png",width,height)
	pixels = img.load()

	t = 0.0
	startx = prevx = x = width/2
	starty = prevy = y =  height/2
	z = 0

	charSizeW = R.randint(32,64)
	charSizeH = R.randint(32,64)
	angle = pi/180.0
	direction = R.random()*pi*2.0
	distance = 6.0

	(r,g,b,a) = (R.randint(128,255),R.randint(0,255),R.randint(0,255),32)
	posY = 0
	while posY < height:
		print posY
		posX = 0
		P = []


		while posX < width:
			P.append((posX,posY+charSizeH,0))
			maxP = 13
			if R.randint(1,100) > 90:
				maxP = 17
			for i in xrange(3,maxP):
				P.append((R.randint(posX,posX+charSizeW),R.randint(posY,posY+charSizeH),0)) # apply the wiggle when rendering, not when calculating
			P.append((posX+charSizeW,posY+charSizeH,0))

			posX = posX+charSizeW
		P = calcLinesSmooth(SMOOTHAMOUNT,P)
		P = makePathUnique(P)

		for (x,y,z) in P:
			radius = abs(cos(direction)*maxRadius)
			#print radius
			try:
				drawPixelAddAlpha(pixels,r,g,b,a,x,y)
			except:
				error = error +1
				# print "Plot error 1 "+str(x+posX)+" "+str(y+posY)
			try:
				drawPointInky(pixels,int(radius),r,g,b,a,x,y)
			except:
				error = error +1
				#print "Plot error 2 "+str(x+posX)+" "+str(y+posY)
			if R.random() > 0.995:
				try:
					drawPointInkyDrops(pixels,R.randint(1,maxRadius*3),r,g,b,1,x,y) # Add noise to x and y?
				except:
					error = error +1
					# print "Plot error 3 "+str(x+posX)+" "+str(y+posY)
				# drawLineInkySplodge(pixels,direction,distance,r,g,b,a,x,y)

			direction = direction+angle #spin
			distance = distance+0.3*float(R.randint(-1,1))
			if distance > 48:
				distance = 48
			if distance < 8:
				distance = 8
			#if R.random() > R.random():
			#	drawPointInkyMessy(pixels,radius,r,g,b,a,x,y)
			r = r+R.randint(-1,1)
			g = g+R.randint(-1,1)
			b = b+R.randint(-1,1)
			if r > 255:
				r = 255
			if r < 0:
				r = 0
			if g > 255:
				g = 255
			if g < 0:
				g = 0
			if b > 255:
				b = 255
			if b < 0:
				b = 0
			
		posY = posY+charSizeH
	
	
#	if R.random() > 0.5:
#		thresholdAbove(img, 100,100,100,0, 0,0,0,0)
	invertPixels(img)
	return img
	
def InkSplodgyWiggleLines(img): # Reference
	width = img.size[0]
	height = img.size[1]

	error = 0
	R = Random()
	SMOOTHAMOUNT = 4
	maxRadius = 4 # int(width/20)
	border = 3*maxRadius
#	(filename,width,height) = ("ajb_example_InkSplodgyWiggleLines_"+str(SEED)+"_"+str(randint(10000000,99999999))+".png",width,height)
#	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	(r,g,b,a) = (R.randint(128,255),R.randint(0,255),R.randint(0,255),32)


	t = 0.0
	startx = prevx = x = width/2
	starty = prevy = y =  height/2
	z = 0

	charSizeW = R.randint(16,64)
	charSizeH = R.randint(16,64)

	posY = 0
	while posY < height:
		posX = 0
		while posX < width:
			P = []
			P.append((0,charSizeH,0))
			maxP = 17
			if R.randint(1,100) > 90:
				maxP = 13
			for i in xrange(5,maxP):
				P.append((R.randint(0,charSizeW),R.randint(0,charSizeH),0)) # apply the wiggle when rendering, not when calculating
			P.append((charSizeW,charSizeH,0))
			angle = pi/180.0
			P = calcLinesSmooth(SMOOTHAMOUNT,P)
			P = makePathUnique(P)
			direction = R.random()*pi*2.0
			distance = 6.0

			for (x,y,z) in P:
				radius = R.randint(1,maxRadius)
				try:
					drawPixelAddAlpha(pixels,r,g,b,a,x+posX,y+posY)
					if R.random() > 0.999:
						drawPointInkyDrops(pixels,radius,r,g,b,1,x+posX,y+posY) # Add noise to x and y?
					# drawLineInkySplodge(pixels,direction,distance,r,g,b,a,x,y)
					direction = direction+angle #spin
					distance = distance+0.3*float(R.randint(-1,1))
					if distance > 48:
						distance = 48
					if distance < 8:
						distance = 8
					#if R.random() > R.random():
					#	drawPointInkyMessy(pixels,radius,r,g,b,a,x,y)
				except:
#					print "Plot error "+str(x+posX)+" "+str(y+posY)
					error = error + 1
			posX = posX+charSizeW
			
		posY = posY+charSizeH
	
	
#	if R.random() > 0.5:
#		thresholdAbove(img, 100,100,100,0, 0,0,0,0)
	invertPixels(img)
#	img.save(filename)
#	print filename
#	print "Complete"
	return img
	
def InkSplodgyLineSpiralWiggleLines(img): # Reference
	width = img.size[0]
	height = img.size[1]

	error = 0
	R = Random()
	SMOOTHAMOUNT = 4

	maxRadius = 4 # int(width/20)
	border = 3*maxRadius
#	(filename,width,height) = ("ajb_example_InkSplodgyLineSpiralWiggleLines_"+str(SEED)+"_"+str(randint(10000000,99999999))+".png",width,height)
#	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	(r,g,b,a) = (R.randint(128,255),R.randint(0,255),R.randint(0,255),32)

	P = []

	t = 0.0
	startx = prevx = x = width/2
	starty = prevy = y =  height/2
	z = 0
	
	count = 0
	angle = pi/180.0
	while x < width and x > 0 and y < height and y > 0 and count < 1000000:
		count = count + 1
		wigglex = R.randint(-maxRadius,maxRadius)
		wiggley = R.randint(-maxRadius,maxRadius)

		x = startx+t/10*cos(t*angle)
		y = starty+t/10*sin(t*angle)
		t = t+0.1
		
		if prevx != int(x) and prevy != int(y): # and count%10 == 0: # new point please, offset a little thanks!
			P.append((x+wigglex,y+wiggley,0)) # apply the wiggle when rendering, not when calculating
			prevx = int(x)
			prevy = int(y)

	
	P = calcLinesSmooth(SMOOTHAMOUNT,P)
	P = makePathUnique(P)
	direction = R.random()*pi*2.0
	distance = 6.0
	for (x,y,z) in P:
		if R.random() > R.random():
			radius = R.randint(1,maxRadius)
			if x <= border:
				x = border+1
			if x >= width-2-border:
				x = width-2-border
			if y <= border:
				y = border+1
			if y >= height-2-border:
				y = height-2-border
			try:
				drawPixelAddAlpha(pixels,r,g,b,a,x,y)
				drawPointInkyDrops(pixels,radius,r,g,b,a,x,y) # Add noise to x and y?
				drawLineInkySplodge(pixels,direction,distance,r,g,b,a,x,y)
				direction = direction+angle #spin
				distance = distance+0.3*float(R.randint(-1,1))
				if distance > 48:
					distance = 48
				if distance < 8:
					distance = 8
				#if R.random() > R.random():
				#	drawPointInkyMessy(pixels,radius,r,g,b,a,x,y)
			except:
				error = error + 1
				#print "Plot error "+str(x)+" "+str(y)
	
	if R.random() > 0.5:
		thresholdAbove(img, 100,100,100,0, 0,0,0,0)
	invertPixels(img)
	return img
	
def InkSplodgyLineSpiralWiggle(img): # Reference
	width = img.size[0]
	height = img.size[1]
	error = 0
	R = Random()
	SMOOTHAMOUNT = 4
	maxRadius = 4 # int(width/20)
	border = 3*maxRadius
#	(filename,width,height) = ("ajb_example_InkSplodgyLineSpiralWiggle_"+str(SEED)+"_"+str(randint(10000000,99999999))+".png",width,height)
#	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	(r,g,b,a) = (R.randint(128,255),R.randint(0,255),R.randint(0,255),32)

	P = []

	t = 0.0
	startx = prevx = x = width/2
	starty = prevy = y =  height/2
	z = 0
	
	count = 0
	angle = pi/180.0
	while x < width and x > 0 and y < height and y > 0 and count < 1000000:
		count = count + 1
		wigglex = R.randint(-maxRadius,maxRadius)
		wiggley = R.randint(-maxRadius,maxRadius)

		x = startx+t/10*cos(t*angle)
		y = starty+t/10*sin(t*angle)
		t = t+0.1
		
		if prevx != int(x) and prevy != int(y): # and count%10 == 0: # new point please, offset a little thanks!
			P.append((x+wigglex,y+wiggley,0)) # apply the wiggle when rendering, not when calculating
			prevx = int(x)
			prevy = int(y)

	
	P = calcLinesSmooth(SMOOTHAMOUNT,P)
	P = makePathUnique(P)
	for (x,y,z) in P:
		if R.random() > 0.0:
			radius = R.randint(1,maxRadius)
			if x <= border:
				x = border+1
			if x >= width-2-border:
				x = width-2-border
			if y <= border:
				y = border+1
			if y >= height-2-border:
				y = height-2-border
			try:
				drawPixelAddAlpha(pixels,r,g,b,a,x,y)
				#drawPointInkyDrops(pixels,radius,r,g,b,a,x,y) # Add noise to x and y?
				if R.random() > R.random():
					drawPointInkyMessy(pixels,radius,r,g,b,a,x,y)
			except Error:
#				print "Plot error "+str(x)+" "+str(y)
				error=error+1
	if R.random() > 0.5:
		thresholdAbove(img, 100,100,100,0, 0,0,0,0)
	invertPixels(img)
#	img.save(filename)
#	print filename
#	print "Complete"
	return img

def InkSplodgyLineSpiral(img): # Reference
	width = img.size[0]
	height = img.size[1]
	error = 0
	R = Random()
	SMOOTHAMOUNT = 4
	maxRadius = 4 # int(width/20)
	border = 3*maxRadius
#	(filename,width,height) = ("ajb_example_InkSplodgyLineSpiral_"+str(SEED)+"_"+str(randint(10000000,99999999))+".png",width,height)
#	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	(r,g,b,a) = (R.randint(128,255),R.randint(0,255),R.randint(0,255),32)

	P = []
#	gap = 30

#	for x in xrange(0,width):
#		t = float(gap)/float(width)*x
#		if x%gap == 0:
#			for y in xrange(0,height):
#				if y%gap == 0:
#					P.append((x+R.randint(-int(t),int(t)),y,0))
	
#	P.append((0,0,0))
#	P.append((width,0,0))
#	P.append((width,height,0))
#	P.append((0,height,0))
#	P.append((0,0,0))
#	P.append((width,0,0))

	t = 0.0
	startx = prevx = x = width/2
	starty = prevy = y =  height/2
	z = 0
	
	gap1 = R.randint(5,20)
	gap2 = gap1
	if R.randint(1,100) > 50:
		gap2 = R.randint(5,20)
	
	count = 0
	angle = pi/180.0
	while x < width and x > 0 and y < height and y > 0 and count < 1000000:
		count = count + 1
		x = startx+t/gap1*cos(t*angle)
		y = starty+t/gap2*sin(t*angle)
		t = t+0.1
		
		if prevx != int(x) and prevy != int(y): # and count%10 == 0: # new point please, offset a little thanks!
			P.append((x,y,0))			
			prevx = int(x)
			prevy = int(y)

	
	P = calcLinesSmooth(SMOOTHAMOUNT,P)
	P = makePathUnique(P)
	for (x,y,z) in P:
		if R.random() > 0.0:
			radius = R.randint(1,maxRadius)
			if x <= border:
				x = border+1
			if x >= width-2-border:
				x = width-2-border
			if y <= border:
				y = border+1
			if y >= height-2-border:
				y = height-2-border
			try:
				drawPixelAddAlpha(pixels,r,g,b,a,x,y)
				#drawPointInkyDrops(pixels,radius,r,g,b,a,x,y) # Add noise to x and y?
				if R.random() > R.random():
					drawPointInkyMessy(pixels,radius,r,g,b,a,x,y)
			except Error:
				error=error+1
				# print "Plot error "+str(x)+" "+str(y)
	
	if R.random() > 0.5:
		thresholdAbove(img, 100,100,100,0, 0,0,0,0)
	invertPixels(img)
#	img.save(filename)
#	print filename
#	print "Complete"
	return img
	
def InkSplodgy(img):
	width = img.size[0]
	height = img.size[1]
	error = 0
	R = Random()
	maxRadius = int(width/50)
	border = 3*maxRadius
#	(filename,width,height) = ("ajb_example_InkSplodgy"+"_"+str(SEED)+"_"+str(randint(10000000,99999999))+".png",width,height)
#	img = Image.new('RGBA', (width, height))
	pixels = img.load()
	(r,g,b,a) = (R.randint(128,255),R.randint(0,255),R.randint(0,255),64)
	for i in xrange(0,R.randint(1,width+height)):
		radius = R.randint(1,maxRadius)
		px = R.randint(border,width-2-border)
		py = R.randint(border,height-2-border)
		
		if px <= radius:
			px = radius+1
		if px >= width-2-radius:
			px = width-2-radius
		if py <= radius:
			py = radius+1
		if py >= height-2-radius:
			py = height-2-radius
		# print radius,r,g,b,a,px,py
		#drawPointInkyMessy(pixels,radius,r,g,b,a,px,py)
		drawPointInkyDrops(pixels,radius,r,g,b,a,px,py)

	if R.random() > 0.5:
		thresholdAbove(img, 100,100,100,0, 0,0,0,0)
	invertPixels(img)
#	img.save(filename)
#	print filename
#	print "Complete"
	return img

def invertPixels(img):
	pixels = img.load()
	width = img.size[0]
	height = img.size[1]	
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pixels[x,y]
			pixels[x,y] = (255-r,255-g,255-b,255-a)

def invertPixelsNotAlpha(img):
	pixels = img.load()
	width = img.size[0]
	height = img.size[1]	
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pixels[x,y]
			pixels[x,y] = (255-r,255-g,255-b,a)
	
			
def thresholdAbove(img,r0,g0,b0,a0,r1,g1,b1,a1):
	pixels = img.load()
	width = img.size[0]
	height = img.size[1]	
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pixels[x,y]
			if r < r0 or g < g0 or b < b0 or a < a0:
				pixels[x,y] = (r1,g1,b1,a1)
	
def drawFeltTipPen(pixels,R,radius,r,g,b,a,x,y):
	error = 0
	try:
		drawPixelAddAlpha(pixels,r,g,b,a,x,y)
	except:
		error = error+1
		# print "Plot error 1 "+str(x)+" "+str(y)
	if R.random() > 0.995:
		try:
			drawPointInky(pixels,int(radius),r,g,b,a,x,y)
		except:
			error = error+1
			# print "Plot error 2 "+str(x)+" "+str(y)
	if R.random() > 0.995:
		try:
			drawPointInkyDrops(pixels,R.randint(1,radius*3),r,g,b,1,x,y) # Add noise to x and y?
		except:
			error = error+1
			# print "Plot error 3 "+str(x)+" "+str(y)
		# drawLineInkySplodge(pixels,direction,distance,r,g,b,a,x,y)

def scaleToMaxIntensity(img):
	width = img.size[0]
	height = img.size[1]
	cw = width>>1
	ch = height>>1
	r2 = cw**2
	pix = img.load()
	for x in xrange(0,width):
		dx = x-cw
		dx2 = dx**2
		for y in xrange(0,height):
			dy = y-ch
			dy2 = dy**2
			if dx2+dy2 > r2:
				(r,g,b,a) = pix[x,y]
				pix[x,y] = (r,g,b,0)	
	
def circlePic(img):
	width = img.size[0]
	height = img.size[1]
	cw = width>>1
	ch = height>>1
	r2 = cw**2
	pix = img.load()
	for x in xrange(0,width):
		dx = x-cw
		dx2 = dx**2
		for y in xrange(0,height):
			dy = y-ch
			dy2 = dy**2
			if dx2+dy2 > r2:
				(r,g,b,a) = pix[x,y]
				pix[x,y] = (r,g,b,0)
		
def collapseAlpha(img):
	width = img.size[0]
	height = img.size[1]
	
	pix = img.load()
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pix[x,y]
			pix[x,y] = (r,g,b,255)

def checkAverageAlpha(img):
	width = img.size[0]
	height = img.size[1]
	
	pix = img.load()
	val = 0
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = pix[x,y]
			val = val + a
	avg = a/(width*height)
	return avg

def drawCircleSmooshy(img,radius,r,g,b,a,x,y,z):
	return img

def drawPointInkyDrops(pixels,radius,r,g,b,a,x,y):
	R = Random()
	radiusO = radius
	for i in xrange(0,R.randint(1,3)):
		tr = int(radiusO/(i+1))
		if tr < 1:
			tr = 1
		radius = abs(R.randint(1,tr)+1)
		a = a - R.randint(1,16)
		if a < 16:
			a = 16
		dx = R.randint(-2*radiusO,2*radiusO)
		dy = R.randint(-2*radiusO,2*radiusO)
#		print x,y,dx,dy,x+dx,y+dy
		drawPointInky(pixels,radius,r,g,b,a,x+dx,y+dy)

def drawLineInky(pixels,direction,distance,r,g,b,a,x,y):
	for i in xrange(0,int(distance)):
		posx = x+float(i)*cos(direction)
		posy = y+float(i)*sin(direction)
		drawPixelAddAlpha(pixels,r,g,b,a,posx,posy)

def drawLineInkySplodge(pixels,direction,distance,r,g,b,a,x,y):
	for i in xrange(0,int(distance)):
		posx = x+float(i)*cos(direction)
		posy = y+float(i)*sin(direction)
		drawPixelAddAlpha(pixels,r,g,b,a,posx,posy)
		if random() > random():
			drawPointInkyDrops(pixels,distance-i,r,g,b,a,x,y)
	
def drawPointInkyMessy(pixels,radius,r,g,b,a,x,y):
	R = Random()
	radiusO = radius
	for i in xrange(0,R.randint(1,7)):
		tr = radiusO-i
		if tr < 1:
			tr = 1
		radius = abs(R.randint(1,tr)+1)
		a = a - R.randint(1,16)
		if a < 1:
			a = 1
		dx = R.randint(-radius,radius)
		dy = R.randint(-radius,radius)
		drawPointInky(pixels,radius,r,g,b,a,x+dx,y+dy)
	
def drawPointInky(pixels,radius,r,g,b,a,x,y):
	#pixels = img.load()
	# draw a blob here
	radiusSq = radius*radius
	for x0 in xrange(-radius,radius+1):
		for y0 in xrange(-radius,radius+1):
			if (x0**2 + y0**2) <= radiusSq:
				drawPixelAddAlpha(pixels,r,g,b,a,x+x0,y+y0)

def drawPixelAddAlpha(pixels,r,g,b,a,x,y):
	#print x,y
	(r0,g0,b0,a0) = pixels[x,y]
	r1 = r0+r
	g1 = g0+g
	b1 = b0+b
	a1 = a0+a
	if r1 > 255:
		r1 = 255
	if g1 > 255:
		g1 = 255
	if b1 > 255:
		b1 = 255
	if a1 > 255:
		a1 = 255
	pixels[x,y] = (r1,g1,b1,a1)

def drawPixel(pixels,r,g,b,a,x,y):
	pixels[x,y] = (r,g,b,a)	

#	pixels[x,y] = ((r0+r)%0xff,(g0+g)%0xff,(b0+b)%0xff,(a0+a)%0xff)

def intToCircle(i,max):
	j = float(2.0*pi * float(i) / float(max) )
	return j%max
	
def drawLine(scratchpad, block, p, q ):
	drawLineConstrained(scratchpad, block, p, q, 0 )

def drawLineWithAlpha(scratchpad, block, p, q ):
	drawLineConstrainedWithAlpha(scratchpad, block, p, q, 0 )
	
def drawLineConstrained(pixels, b, p, q, maxLength ):
	(blockID, blockData) = b
	(x,y,z) = p
	(x1,y1,z1) = q
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dy*dy
	distance = sqrt(dz*dz + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dz, sqrt(distHoriz))
		theta = atan2(dy, dx)

		iter = 0
		while iter <= distance:
			setBlock(pixels,(blockID,blockData),((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(theta)*cos(phi)), (int)(z+iter*sin(phi)) ))
			iter = iter+0.5 # slightly oversample because I lack faith.
			
def drawLineConstrainedWithAlpha(pixels, b, p, q, maxLength ):
	(blockID, blockData) = b
	(x,y,z) = p
	(x1,y1,z1) = q
	(r0,g0,b0,a0) = blockID
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			x2 = (int)(x+iter*cos(theta)*cos(phi))
			y2 = (int)(y+iter*sin(phi))
			z2 = (int)(z+iter*sin(theta)*cos(phi))
			(r,g,b,a) = pixels[x2,y2]
			if a > 0:
				a = a-1
			setBlock(pixels,(((r0+r)%0xff,(g0+g)%0xff,(b0+b)%0xff,(a)%0xff),blockData),(x2, y2, z2))
			iter = iter+0.5 # slightly oversample because I lack faith.
			
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
			
def setBlock(pixels,b,p):
	# (mx,my) = pixels
	(ID,Data) = b
	(x,y,z) = p

	pixels[x,y] = ID
	
def Factorise(number):
	Q = []
	
	n = number
	
	for iter in xrange(1,(int)(n)):
		p = (int)(n/iter)
		if n - (p * iter) == 0:
			if iter not in Q:
				Q.append(iter)
			if p not in Q:
				Q.append(p)
	return Q
		
def makePathUnique(P):
	Q = []
	(prevX,prevY,prevZ) = (int(-1),int(-1),int(-1)) # Dummy
	for (x,y,z) in P:
		if (int(x),int(y),int(z)) != (int(prevX),int(prevY),int(prevZ)):
			Q.append((x,y,z))
			(prevX,prevY,prevZ) = (int(x),int(y),int(z))
#		else: # Debug
#			print "Duplicate discarded: "+str(x)+",	"+str(y)+", "+str(z)
	return Q
	
def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result
	
# Ye Olde GFX Libraries
def cosineInterpolate(a, b, x): # http://www.minecraftforum.net/forums/off-topic/computer-science-and-technology/482027-generating-perlin-noise?page=40000
	ft = pi * x
	f = ((1.0 - cos(ft)) * 0.5)
	ret = float(a * (1.0 - f) + b * f)
	return ret

def cnoise(x,y,z):
	# Return the value of interpolated noise at this location
	return float(Random(x+(y<<4)+(z<<8)).random())

def noise(x,y,z):
	ss = 8
	bs = 3
	cx = x >> bs
	cy = y >> bs
	cz = z >> bs

	rdx = float((float(x%ss))/ss)
	rdy = float((float(y%ss))/ss)
	rdz = float((float(z%ss))/ss)
#	print rdx,rdy,rdz
	
	# current noise cell
	P = zeros((2,2,2))
	for iy in xrange(0,2):
		for iz in xrange(0,2):
			for ix in xrange(0,2):
				P[ix,iy,iz] = float(cnoise(cx+ix,cy+iy,cz+iz))
	
	# print P

	dvx1 = cosineInterpolate(P[0,0,0],P[1,0,0],rdx)
	dvx2 = cosineInterpolate(P[0,1,0],P[1,1,0],rdx)
	dvx3 = cosineInterpolate(P[0,0,1],P[1,0,1],rdx)
	dvx4 = cosineInterpolate(P[0,1,1],P[1,1,1],rdx)

	dvz1 = cosineInterpolate(dvx1,dvx3,rdz)
	dvz2 = cosineInterpolate(dvx2,dvx4,rdz)

	n = cosineInterpolate(dvz1,dvz2,rdy)
	
	return n

def drawTriangle(level, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def drawTriangleEdge(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge):
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def calcLine((x,y,z), (x1,y1,z1) ):
	return calcLineConstrained((x,y,z), (x1,y1,z1), 0 )
			
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

def cosineInterpolate(a, b, x): # http://www.minecraftforum.net/forums/off-topic/computer-science-and-technology/482027-generating-perlin-noise?page=40000
	ft = pi * x
	f = ((1.0 - cos(ft)) * 0.5)
	ret = float(a * (1.0 - f) + b * f)
	return ret
	
def cnoise(x,y,z):
	# Return the value of interpolated noise at this location
	return float(Random(x+(y<<4)+(z<<8)).random())

def noise(x,y,z):
	ss = 8
	bs = 3
	cx = x >> bs
	cy = y >> bs
	cz = z >> bs

	rdx = float((float(x%ss))/ss)
	rdy = float((float(y%ss))/ss)
	rdz = float((float(z%ss))/ss)
#	print rdx,rdy,rdz
	
	# current noise cell
	P = zeros((2,2,2))
	for iy in xrange(0,2):
		for iz in xrange(0,2):
			for ix in xrange(0,2):
				P[ix,iy,iz] = float(cnoise(cx+ix,cy+iy,cz+iz))
	
	# print P

	dvx1 = cosineInterpolate(P[0,0,0],P[1,0,0],rdx)
	dvx2 = cosineInterpolate(P[0,1,0],P[1,1,0],rdx)
	dvx3 = cosineInterpolate(P[0,0,1],P[1,0,1],rdx)
	dvx4 = cosineInterpolate(P[0,1,1],P[1,1,1],rdx)

	dvz1 = cosineInterpolate(dvx1,dvx3,rdz)
	dvz2 = cosineInterpolate(dvx2,dvx4,rdz)

	n = cosineInterpolate(dvz1,dvz2,rdy)
	
	return n