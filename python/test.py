#!/usr/bin/env python

import argparse
import os
import sys
import time


from time import gmtime, strftime

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
flat = cv2.imread('flat16sun.tif',-1)

print type(flat)
print flat


debayer = cv2.cvtColor(np.uint16(np.clip(flat,0,65535)), cv2.COLOR_BayerRG2RGB )
#debayer = cv2.cvtColor(np.uint16(np.clip(pre,0,65535)), cv2.COLOR_BayerGR2RGB ) #120



