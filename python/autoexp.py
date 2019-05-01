#!/usr/bin/env python

import argparse
import os
import sys
import time
import zwoasi as asi


import cv2
import numpy as np
from PIL import Image


flat = cv2.imread('flat16.tif',-1)

print type(flat)
print flat

Favg = np.average(flat)

print Favg

flat=Favg/flat

print flat



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

# Get all of the camera controls
#print('')
#print('Camera controls:')
controls = camera.get_controls()
#for cn in sorted(controls.keys()):
    #print('    %s:' % cn)
    #for k in sorted(controls[cn].keys()):
        #print('        %s: %s' % (k, repr(controls[cn][k])))


# Use minimum USB bandwidth permitted
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MaxValue'])

# Set some sensible defaults. They will need adjusting depending upon
# the sensitivity, lens and lighting conditions used.
camera.disable_dark_subtract()

#camera.auto_exposure()
#camera.start_video_capture()

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
camera.set_control_value(asi.ASI_GAMMA, 100)
camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
camera.set_control_value(asi.ASI_FLIP, 0)

camera.set_control_value(controls['AutoExpMaxExpMS']['ControlType'], 20000)
camera.set_control_value(controls['HardwareBin']['ControlType'], controls['HardwareBin']['MinValue'])



exp=100000

for x in range(0, 100):

	camera.set_control_value(asi.ASI_EXPOSURE, exp)
	print('Capturing a single 16-bit mono image')
	filename = 'image_mono16.tiff'

	imagey = camera.capture()
	#imagey = camera.capture_video_frame()
	#camera.capture(filename=filename)

	print type(imagey)

	#print imagey

	min =np.amin(imagey)
	max=np.amax(imagey)
	average=np.average(imagey)
	median=np.median(imagey)

	qt1=np.percentile(imagey,50)
	qt2=np.percentile(imagey,75)
	qt3=np.percentile(imagey,95)

	print min
	print max
	print average
	print median
	print qt1
	print qt2
	print qt3
	
	if qt3>(256*250):
		exp=int(exp/1.2)
		print "new exp"
		print exp
	elif qt3<(256*200):
		exp=int(exp*1.2)
		print "new exp"
		print exp
	else:

		#with np.nditer(imagey, op_flags=['readwrite']) as it:
			#for x in it:
				#x[...] = x/256
				#x[...]=255*(((x/(x+a))-ddpmin)/ddpmm)
				#x[...]=20000*((x/float(x+a))/b)
				
		#print imagey

		#im = Image.fromarray(imagey).convert('RGB')
		
		#data = np.asarray(im)
		#im = Image.fromarray(np.roll(data, 1, axis=-1))
		
		
		
		##b, g, r = im.split()
		##im = Image.merge("RGB", (r, g, b))
		
		#print type(imagey)
		#print imagey
		
		##imagey=
		
		#im = Image.fromarray(imagey*flat)
		
		#debayer = cv2.cvtColor(imagey, cv2.COLOR_BayerGB2RGB )
		#debayer = cv2.cvtColor(imagey, cv2.COLOR_BayerBG2RGB )
		debayer = cv2.cvtColor(np.uint16(np.clip(imagey*flat,0,65535)), cv2.COLOR_BayerRG2RGB )
		
		cv2.imwrite("your_file2-rgb.tif", debayer)
		
		##im = Image.fromarray(debayer)

		#idebayer.save("your_file2-rgb.tif")
		
		break

