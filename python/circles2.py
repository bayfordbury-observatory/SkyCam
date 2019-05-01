#!/usr/bin/env python

import argparse
import os
import sys
import time

print "---------"
import math

print "ok"

#from scipy.ndimage.filters import convolve

print "cv2"

import cv2

print "numpy"
import numpy as np

print "PIL"
from PIL import Image

#print "tstack"
#from colour.utilities import tstack

#print "CFA"
#from colour_demosaicing.bayer import masks_CFA_Bayer


print "---------"

hough = np.zeros((960*2, 1280*2), np.uint16)

accum = np.zeros((960*2, 1280*2, 50))


#debayer = cv2.resize(cv2.cvtColor(np.uint8(np.clip(pre/256,0,255)), cv2.COLOR_BayerRG2RGB ), (0,0), fx=0.5, fy=0.5) 
debayer = cv2.imread('Capture_00001.tif',1)

print(debayer[800][600])

gray_image = cv2.cvtColor(debayer, cv2.COLOR_RGB2GRAY)

#gray_image= cv2.GaussianBlur(gray_image,(5,5),0)

#gray_image = cv2.medianBlur(gray_image,5)
	
#gray_image=(float(gray_image - min) / (max - min))*255
#gray_image=cv2.equalizeHist(gray_image)


cimg = gray_image
canny = 50

edges = cv2.Canny(gray_image,10,canny)

print edges.shape

print "detecting circles" 

for x in range(0, 1280):
	for y in range(0, 960):
		val = edges[y,x]
		#print val
		if val > 0:
			for r  in range (210,230): # the possible radius
				for t  in range (0,360):  # the possible  theta 0 to 360 
					a = int(x - r * math.cos(t * math.pi / 180)) #polar coordinate for center
					b = int(y - r * math.sin(t * math.pi / 180))  #polar coordinate for center 
					if a> -640 and a< (1280+640) and b > -480 and b<(960+480):
						accum[b+480, a+640, r-200] +=1# //voting
						hough[b+480, a+640]+=1

max= np.max(accum)		

print max			

for x in range(0, 1280*2):
	for y in range(0, 960*2):
		for r  in range (210,230):
			if max==accum[y, x, r-200]:
				print str(x/2)+" "+str(y/2)+ " "+str(r)
				peakx = x
				peaky = y
				peakr = r


print "done"
#if circles is not None:

	#circles = np.uint16(np.around(circles))
	#print "detected circles"
	#for i in circles[0,:]:
		# draw the outer circle
		#print("circle at "+str((i[0]*2))+" "+str(i[1])+" "+str(i[2]))
		
cv2.imwrite("hough.tif", hough)
		
cv2.circle(debayer,(peakx-640, peaky-480), peakr,(0,255,0),2)
		# draw the center of the circle
cv2.circle(debayer,(peakx-640, peaky-480),2,(0,0,255),3)
		


	
hough = cv2.resize(hough, (0,0), fx=0.5, fy=0.5) 


		
cv2.imshow('circles',hough)
cv2.imshow('orig',debayer)
cv2.imshow('edges',edges)

##im = Image.fromarray(cimg)

#idebayer.save("your_file2-rgb.tif")

cv2.waitKey(0)
cv2.destroyAllWindows()
	
	#time.sleep(2)
#cv2.destroyAllWindows()
