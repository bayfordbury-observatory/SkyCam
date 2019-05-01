from PIL import Image
import numpy as np

import cv2


flat = cv2.imread('flat16sun.tif',-1)
im = cv2.imread('Capture_00004.tiff',-1)


Favg = np.average(flat)

print Favg

flat=Favg/flat

flat = flat-1

flat = flat*2

flat=flat+1


pre = im*flat*0.75

debayer = cv2.cvtColor(np.uint16(np.clip(pre,0,65535)), cv2.COLOR_BayerRG2RGB )

cv2.imwrite("out.tif", debayer)