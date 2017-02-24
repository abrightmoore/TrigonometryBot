# @abrightmoore - see @TrigonometryBot
# This version refactored for extensibility

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
from io import BytesIO
import sys

from PIL import Image, ImageDraw
from TwitterAPI import TwitterAPI # by @boxnumber03 https://dev.twitter.com/resources/twitter-libraries. Wrapper to communicate via Twitter
from markovbot import MarkovBot # by @esdalmaijer. Use for conversation

from Trigpic import *

number = 1000000000
while True:
	img = createImage(400,400)
	id = str(randint(1,99999999999999999))
	img.save("AJImage_"+str(number)+"_"+id+"alpha.png")
	alphaAvg = checkAverageAlpha(img)
	if alphaAvg > 128:
		collapseAlpha(img)
		img.save("AJImage_"+str(number)+"_"+id+".png")
	number = number+1
