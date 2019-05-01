import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

stitcher = cv2.createStitcher(False)

foo = cv2.imread("4.tif")
bar = cv2.imread("3.tif")

result = stitcher.stitch((foo,bar))

#print result

#out = adjust_gamma(result[1],2)

#cv2.imwrite("out.tif", out)
cv2.imwrite("out.tif", result[1])