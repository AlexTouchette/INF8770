# Première étape: Division de la trame en macroblocs --------------------
import numpy as np
import cv2 as cv

vidcap = cv.VideoCapture('bouncing_dvd_logo_1.mp4')


def get_frames():
    success,image = vidcap.read()
    count = 0
    while success:
        cv.imwrite("frame%d.jpg" % count, image) # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1


get_frames()

# On définit la largeur et la hauteur des macroblocs
largeur = 16
hauteur = 16

# On découpe l'image en macroblocs
"""
for l in range(0,test_image.shape[0], largeur):
    for h in range(0,test_image.shape[1], hauteur):
        window = test_image[l:l+largeur,h:h+hauteur]
        hist = np.histogram(window,bins=grey_levels)
        windows.append(window)
"""


