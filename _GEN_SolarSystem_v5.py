# @TheWorldFoundry
# - enhancing the Solar System data structures to support dynamic changes
from math import pi,cos,sin
from random import random, randint
import sys
import pygame
pygame.init()

# Initialise trigonometry tables for speed
ANGLESMAX = 2880
ANGLEQUANTUM = pi*2.0/ANGLESMAX
SIN = []
COS = []
for i in xrange(0,ANGLESMAX): # Precalculate and cache for trigonometry
    ang = ANGLEQUANTUM*i
    SIN.append(sin(ang))
    COS.append(cos(ang))

class Body:
	def __init__(self,label,radiusVisual,imageVisual):
		self.Level = 1
		self.Label = label
		self.Parent = None
		self.Children = [] # Hierarchical tree of bodies
		self.AllChildren = [] # flat list of everything in the system
		self.Exists = True
		self.OrbitRadius = 0
		self.OrbitAngle = 0
		self.OrbitVelocity = 0
		self.OrbitColour = (randint(0x30,0x60),randint(0x10,0x40),randint(0x30,0x60))

		
		# Visual behaviour
		self.Images = []
		self.RadiusVisual = radiusVisual
		self.Images.append(pygame.transform.smoothscale(pygame.image.load(imageVisual+".png"),((radiusVisual<<1)+1,(radiusVisual<<1)+1)))
		self.ImagesAnimationFrame = 0 # Change this for animation
			
	def addChild(self,child): # Parents add children. Children don't attach themselves to parents: that would be weird.
		self.Children.append(child)
		self.AllChildren.append(child)
		child.Parent = self # Who's your daddy?
		if self.Parent: # Add to the flat list of all objects above
			self.Parent.AllChildren.append(child)
			self.Level = self.Parent.Level+1
			child.Level = self.Level+1
			
	def setOrbit(self,radius,angle,velocity):
		self.OrbitRadius = radius
		self.OrbitAngle = angle%ANGLESMAX
		self.OrbitVelocity = velocity

	def tick(self):
		self.OrbitAngle += self.OrbitVelocity
		self.OrbitAngle = self.OrbitAngle%ANGLESMAX
		self.ImagesAnimationFrame += 1
		for child in self.Children: # Tick off the children
			child.tick()		

	def draw(self,surface,origin): # Draws sprite centred on the position nominated
		scale = 1.0
		(cx,cy) = origin
		
        # Plot relative to the origin
		dx = COS[self.OrbitAngle%ANGLESMAX] * self.OrbitRadius
		dy = SIN[self.OrbitAngle%ANGLESMAX] * self.OrbitRadius

		if self.Exists == True: # Don't draw ghosts        
			x = (dx-self.RadiusVisual) * scale
			y = (dy-self.RadiusVisual) * scale
			x = cx + x
			y = cy + y

			surface.blit(self.Images[self.ImagesAnimationFrame%len(self.Images)],[x,y])

		for child in self.Children:
			child.draw(surface,(dx+cx,dy+cy)) # Draw the child offset from this parent location

	def drawOrbit(self,surface,origin): # Draws sprite centred on the position nominated
		#drawOrbits = True
		scale = 1.0
		(cx,cy) = origin
		
        # Plot relative to the origin
		dx = COS[self.OrbitAngle%ANGLESMAX] * self.OrbitRadius
		dy = SIN[self.OrbitAngle%ANGLESMAX] * self.OrbitRadius

		if self.Exists == True: # Don't draw ghosts        
			x = (dx-self.RadiusVisual) * scale
			y = (dy-self.RadiusVisual) * scale
			x = cx + x
			y = cy + y
			if self.OrbitRadius > 1:
				pygame.draw.circle(surface, self.OrbitColour, (int(cx),int(cy)), int(self.OrbitRadius), self.Level)
#			surface.blit(self.Images[self.ImagesAnimationFrame%len(self.Images)],[x,y])

		for child in self.Children:
			child.drawOrbit(surface,(dx+cx,dy+cy)) # Draw the child offset from this parent location
			
			
	def plot(self,surface,origin,colour):
		colorig = colour
		scale = 1.0
		(cx,cy) = origin
		
        # Plot relative to the origin
		dx = COS[self.OrbitAngle%ANGLESMAX] * self.OrbitRadius
		dy = SIN[self.OrbitAngle%ANGLESMAX] * self.OrbitRadius

		if self.Exists == True: # Don't draw ghosts        
			x = (dx-self.RadiusVisual) * scale
			y = (dy-self.RadiusVisual) * scale
			x = cx + x
			y = cy + y
			deltax = randint(-1,1)
			deltay = randint(-1,1)
			x = int(x)
			y = int(y)
			x1 = x+deltax
			y1 = y+deltay
			

			(r,g,b,a) = colour
			g = int(g/(self.Level))
			if deltax != 0:
				r = int(r/abs(deltax))
				g = int(g/abs(deltax))
				b = int(b/abs(deltax))
			if deltay != 0:
				r = int(r/abs(deltay))				
				g = int(g/abs(deltay))				
				b = int(b/abs(deltay))				
			colour = (r,g,b,a)
			
			if x1 >=0 and x1 < surface.get_width() and y1 >=0 and y1 < surface.get_height:
				surface.set_at((x1,y1),colour)
			if x >=0 and x < surface.get_width() and y >=0 and y < surface.get_height:
				surface.set_at((x,y),colorig)
				
		for child in self.Children:
			child.plot(surface,(dx+cx,dy+cy),colour) # Draw the child offset from this parent location
		
		
def makeSolarSystem():
	images = ["Sol","Earth","Moon","Asteroid"] #,"TrigA","TrigB","TrigC","TrigE"]

	starname = "Sol"
	SolarSystem = Body(starname+"ar System", 1, "Sol")
	Sol = Body("Sol", randint(5,200), "Sol")
	Sol.setOrbit(SolarSystem.RadiusVisual+randint(0,100),0,1)
	SolarSystem.addChild(Sol)

	numStars = randint(1,5)
	starVel = randint(1,3)
	starAngle = int(ANGLESMAX/numStars)
	starDist = (numStars-1)*Sol.RadiusVisual+20
	for i in xrange(1,numStars):
		Star = Body(starname+"ar System "+str(i), 1, "Sol")
		Sol = Body("Sol", randint(5,200), "Sol")
		Sol.setOrbit(starDist,i*starAngle,starVel)
		SolarSystem.addChild(Sol)

	
	if True:
		Main = SolarSystem

		for i in xrange(0,randint(3,15)):
			maxR = 100
			velocity = randint(1,18)
			Hub = Main.AllChildren[randint(0,len(Main.AllChildren)-1)] # Pick a planet
			
			distance = Hub.RadiusVisual+randint(20,200)
			velocity = float(maxR-distance) / float(maxR) * float(velocity)
			
			if velocity < 1:
				velocity = 1
			velocity = int(velocity)
			if (Hub.RadiusVisual>>1) > 0:
				Planet = Body("Planet "+str(i),randint(1,(Hub.RadiusVisual>>1)),images[randint(0,len(images)-1)])
				Planet.setOrbit(distance,randint(0,ANGLESMAX),velocity)
			
				Hub.addChild(Planet)
#		SolarSystem.addBody("Asteroid",(randint(asteroid.radius+10,(width>>1)-20),randint(0,ANGLESMAX)),images[randint(1,len(images)-1)],velocity)

#	for i in xrange(100,1000):
#		if randint(1,10) > 6:
#			velocity = randint(-2,8)
#			if velocity == 0:
#				velocity = 1
#			asteroid = solarSystem.allbodies[randint(0,len(solarSystem.allbodies)-1)]
#
#			asteroid.addBody("Asteroid",(randint(asteroid.radius+10,asteroid.radius+20),randint(0,ANGLESMAX)),randint(1,5),images[randint(0,len(images)-1)],velocity)
#		else:
#			size = 1
#			if randint(1,10) > 8:
#				size = 2
#				if randint(1,10) > 8:
#					size = 3
#					if randint(1,10) > 8:
#						size = 4
				
#			solarSystem.addBody("Asteroid",(randint(300,400),randint(0,ANGLESMAX)),size,images[randint(0,len(images)-1)],randint(1,3))

	return SolarSystem
			
def draw(img):
#	SolarSystem = Body("Sun", 100, "Sol")
#	Earth = Body("Earth", 20, "Earth")
#	Moon = Body("Moon", 10, "Moon")
#	Earth.setOrbit(SolarSystem.RadiusVisual+200,0,3)
#	SolarSystem.addChild(Earth)
#	Moon.setOrbit(Earth.RadiusVisual+50,0,7)
#	Earth.addChild(Moon)
#	Moonlet = Body("Moonlet", 4, "Moon")
#	Moonlet.setOrbit(Moon.RadiusVisual+10,0,12)
#	Moon.addChild(Moonlet)
	width = img.size[0]
	height = img.size[1]
	mode = img.mode
	size = img.size
	data = img.tobytes()
	imgs = img.tobytes("raw",'RGBA')
	imgSource = pygame.image.fromstring(imgs, size, mode)

	FILENAME = "SOLARSYSTEMPLOT_"+str(randint(100000000,999999999))

#	PlotImage = pygame.Surface((width, height))	
#	PlotImage.fill((0x0,0x0,0x0))	
#	SketchImage = pygame.Surface((width, height))	
#	SketchImage.fill((0x0,0x0,0x0))	
	SolarSystem = makeSolarSystem()
	
	SolarSystem.drawOrbit(imgSource,(width>>1,height>>1))
	SolarSystem.draw(imgSource,(width>>1,height>>1))
#	SolarSystem.plot(PlotImage,(width>>1,height>>1),(0xff,0xff,0xff,0xff))
#	SolarSystem.draw(SketchImage,(width>>1,height>>1))
	# pygame.image.save(imgSource, FILENAME+"_SolarSystemSrc.png")	
	# print FILENAME+"_SolarSystemSrc.png"
	pix = img.load()
	for y in xrange(0,height):
		for x in xrange(0,width):
			(r,g,b,a) = imgSource.get_at((x,y))
			pix[x,y] = (r,g,b,a)
		
# doit()