from PIL import Image
import numpy as np

import cv2


flat = cv2.imread('flat16sun.tif',-1)
im = cv2.imread('Capture_00003-g',-1)
#im.show()


r,g,b = im.split()

r.save("rp.png","png")
g.save("gp.png","png")
b.save("bp.png","png")

#rf,gf,bf = flat.split()
	#im = Image.merge("RGB", (r, g, b))

Rimarray = np.array(r)
Gimarray = np.array(g)
Bimarray = np.array(b)

flatarray = np.array(flat)

Ravg = np.average(Rimarray)
Gavg = np.average(Gimarray)
Bavg = np.average(Bimarray)

Favg = np.average(flatarray)

print Ravg
print Gavg
print Bavg


Rimarray = np.uint8(np.clip(Favg*Rimarray/flatarray,0,255))
Gimarray = np.uint8(np.clip(Favg*Gimarray/flatarray,0,255))
Bimarray = np.uint8(np.clip(Favg*Bimarray/flatarray,0,255))
#Rimarray = np.uint8(np.divide(Rimarray, flatarray, out=np.zeros_like(Rimarray), where=flatarray!=0)*Favg)
#Rimarray = np.uint8(np.divide(Rimarray, flatarray, out=np.zeros_like(Rimarray), where=flatarray!=0)*Ravg)
#Gimarray = np.uint8(np.divide(Gimarray, flatarray, out=np.zeros_like(Gimarray), where=flatarray!=0)*Gavg)
#Bimarray = np.uint8(np.divide(Bimarray, flatarray, out=np.zeros_like(Bimarray), where=flatarray!=0)*Bavg)

r = Image.fromarray(Rimarray)
g = Image.fromarray(Gimarray)
b = Image.fromarray(Bimarray)

im = Image.merge("RGB", (r, g, b))
im.save("flatted.tif","tiff")

r.save("r.png","png")
g.save("g.png","png")
b.save("b.png","png")