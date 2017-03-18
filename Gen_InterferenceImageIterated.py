from random import randint
import Gen_InterferenceImage


def draw(img):
	iters = randint(2,4)
	for i in xrange(0,iters):
		Gen_InterferenceImage.draw(img)
	return img