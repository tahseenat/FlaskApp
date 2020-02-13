import urllib.request
f = open('00000001.jpg','wb')
f.write(urllib.request.urlopen('http://www.gunnerkrigg.com//comics/00000001.jpg').read())
f.close()

import cv2

img = cv2.imread('00000001.jpg', cv2.IMREAD_UNCHANGED)

print('Original Dimensions : ', img.shape)

scale_percent = 60  # percent of original size
width = 50
height = 50
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)