import cv2
import numpy as np
from PIL import Image

img = cv2.imread('your_file2.tif',0)

debayer = cv2.cvtColor(img, cv2.COLOR_BayerBG2RGB )

print debayer

im = Image.fromarray(debayer)

im.save("your_file2-rgb.tif")