#!/usr/bin/env python

import argparse
import os
import sys
import time

print "---------"
print "importing zwo"
import zwoasi as asi

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

print "read flat"
flat = cv2.imread('flat16.tif',-1)

print type(flat)
print flat

Favg = np.average(flat)

print Favg

flat=Favg/flat

print flat

cv2.namedWindow('edges',cv2.WINDOW_NORMAL)
cv2.namedWindow('circles',cv2.WINDOW_NORMAL)
cv2.namedWindow('orig',cv2.WINDOW_NORMAL)


cv2.resizeWindow('edges', 774,520)
cv2.resizeWindow('circles', 774,520)
cv2.resizeWindow('orig', 774,520)

print "---------"

__author__ = 'Steve Marple'
__version__ = '0.0.22'
__license__ = 'MIT'


env_filename = os.getenv('ZWO_ASI_LIB')

parser = argparse.ArgumentParser(description='Process and save images from a camera')
parser.add_argument('filename',
                    nargs='?',
                    help='SDK library filename')
args = parser.parse_args()

# Initialize zwoasi with the name of the SDK library
if args.filename:
    asi.init(args.filename)
elif env_filename:
    asi.init(env_filename)
else:
    print('The filename of the SDK library is required (or set ZWO_ASI_LIB environment variable with the filename)')
    sys.exit(1)

num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    print('No cameras found')
    sys.exit(0)

cameras_found = asi.list_cameras()  # Models names of the connected cameras

if num_cameras == 1:
    camera_id = 0
    print('Found one camera: %s' % cameras_found[0])
else:
    print('Found %d cameras' % num_cameras)
    for n in range(num_cameras):
        print('    %d: %s' % (n, cameras_found[n]))
    # TO DO: allow user to select a camera
    camera_id = 0
    print('Using #%d: %s' % (camera_id, cameras_found[camera_id]))

camera = asi.Camera(camera_id)
camera_info = camera.get_camera_property()


controls = camera.get_controls()


# Use minimum USB bandwidth permitted

camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MaxValue'])

camera.disable_dark_subtract()

print('Enabling stills mode')
try:
    # Force any single exposure to be halted
    camera.stop_video_capture()
    camera.stop_exposure()
except (KeyboardInterrupt, SystemExit):
    raise
except:
    pass

camera.set_control_value(asi.ASI_GAIN, 50)

#camera.set_image_type(asi.ASI_IMG_RAW8)
#camera.set_image_type(asi.ASI_IMG_RGB24)
camera.set_image_type(asi.ASI_IMG_RAW16)

camera.set_control_value(asi.ASI_WB_B, 78)
camera.set_control_value(asi.ASI_WB_R, 77)
camera.set_control_value(asi.ASI_GAMMA, 150)
camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
camera.set_control_value(asi.ASI_FLIP, 0)

camera.set_control_value(controls['AutoExpMaxExpMS']['ControlType'], 20000)
camera.set_control_value(controls['HardwareBin']['ControlType'], controls['HardwareBin']['MinValue'])





exp=50000

for x in range(0, 100):

	camera.set_control_value(asi.ASI_EXPOSURE, exp)
	print('Capturing a single 16-bit mono image')
	filename = 'image_mono16.tiff'

	imagey = camera.capture()

	#pre = 65535 * ((imagey*flat)/65535)**(1/1.5)
	pre = imagey#65535 * ((imagey)/65535)**(1/1.5)

	#debayer = cv2.resize(cv2.cvtColor(np.uint8(np.clip(pre/256,0,255)), cv2.COLOR_BayerRG2RGB ), (0,0), fx=0.5, fy=0.5) 
	debayer = cv2.cvtColor(np.uint8(np.clip(pre/256,0,255)), cv2.COLOR_BayerRG2RGB )

	gray_image = cv2.cvtColor(debayer, cv2.COLOR_RGB2GRAY)

	gray_image= cv2.GaussianBlur(gray_image,(5,5),0)
	
	gray_image = cv2.medianBlur(gray_image,5)
		
	#gray_image=(float(gray_image - min) / (max - min))*255
	#gray_image=cv2.equalizeHist(gray_image)
	
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	gray_image = clahe.apply(gray_image)
	
	cimg = gray_image
	
	canny = 50

	circles = cv2.HoughCircles(gray_image,cv2.HOUGH_GRADIENT,1,100, param1=canny,param2=50,minRadius=0,maxRadius=0)
	
	edges = cv2.Canny(gray_image,10,canny)
	
	if circles is not None:

		circles = np.uint16(np.around(circles))

		for i in circles[0,:]:
			# draw the outer circle
			print("circle at "+str((i[0]*2))+" "+str(i[1])+" "+str(i[2]))
			
			cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
			
	cimg = cv2.resize(cimg, (0,0), fx=0.5, fy=0.5) 
	debayer = cv2.resize(debayer, (0,0), fx=0.5, fy=0.5) 
	edges = cv2.resize(edges, (0,0), fx=0.5, fy=0.5) 

	cv2.imshow('circles',cimg)
	#cv2.imshow('orig',debayer)
	#cv2.imshow('edges',edges)

	##im = Image.fromarray(cimg)

	#idebayer.save("your_file2-rgb.tif")

	cv2.waitKey(2000)
	
	#time.sleep(2)
#cv2.destroyAllWindows()
