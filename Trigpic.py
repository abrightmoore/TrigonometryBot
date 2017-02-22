# @abrightmoore

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

	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))
	# Choose what type of image to create
	chance = random()
	if chance < 0.1:
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
	elif chance < 0.12: # A curvy graph
		print "Making a TrigFuncGraphImage"
		makeTrigFuncGraphImage(img,formulaR,formulaG,formulaB)
	elif chance < 0.2:
		print "Making a ColourSwatch"
		makeColourSwatch(img)
	elif chance < 0.4:
		print "Making an InterferenceImage"
		makeInterferenceImage(img)
	elif chance < 0.8:
		print "Making a blendedImage"
		ox,oy,sx,sy = (-2.0,-1.5,3.0,3.0)
#               ox,oy,sx,sy = (-1.108,-0.230,0.005,0.005)
		methods = ["Circle","Spike"]
		imgArray = []
		for i in xrange(0,8):
			(new_ox,new_oy,new_sx,new_sy) = drawMandelbrot(img,ox,oy,sx,sy)
			filename = "AJTrimage_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+formulaR+"_"+formulaG+"_"+formulaB+".png"
			# img.save(filename)
			trigImg = Image.new('RGBA', size=(width, height), color=(0, 0, 0))
			(formulaR,formulaG,formulaB) = getFormulas()
			makeTrigImage(trigImg,formulaR,formulaG,formulaB)
			trigImg.save("AJFractrigMooshyimage_"+str(randint(111111111,999999999))+".png")

			newimg = mergeImages(img,trigImg, "Spike" ) # methods[randint(0,len(methods)-1)])
			newimg.save("AJFractrigimage_"+str(randint(111111111,999999999))+".png")
			ox = new_ox
			oy = new_oy
			sx = new_sx
			sy = new_sy
			imgArray.append(newimg)
		if len(imgArray) > 0:
			img = imgArray[randint(1,len(imgArray)-1)] # Choose one of the images generated
		# for imgA in imgArray:
			# filename = "AJMandelbrot_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+str(randint(111111111,999999999))+".png"
			# imgA.save(filename)
	else:
		print "Making a TrigImage"
		makeTrigImage(img,formulaR,formulaG,formulaB)
	return img

def createImgFile(width,height,author):
	# In memory file method used is by Rolo http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
	FILENAMEIMAGE = '@abrightmoore_@TrigonometryBot_output.png'

	img = Image.new('RGBA', size=(width, height), color=(0, 0, 0))

	# Choose what type of image to create
	chance = random()
	if chance < 0.05:
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
		for imgA in imgArray:
			filename = "AJMandelbrot_"+str(width)+"_"+str(ox)+"_"+str(oy)+"_"+str(sx)+"_"+str(sy)+"_"+str(randint(111111111,999999999))+".png"
			imgA.save(filename)
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
					pix[x,y] = pix2[x,y]
				else: # blend
					(r1,g1,b1,a1) = pix1[x,y]
					(r2,g2,b2,a2) = pix2[x,y]
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