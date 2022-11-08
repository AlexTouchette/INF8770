# Première étape: Division de la trame en macroblocs --------------------
import numpy as np
import cv2 as cv

def get_frames(start_time, end_time):
    success=True
    # read video 
    vidcap = cv.VideoCapture('TP2/bouncing_dvd_logo_1.mp4') 

    # get number of frames per sec ()
    fps = vidcap.get(cv.CAP_PROP_FPS)

    # calculate start frame id and end frame id 
    start_frame_id = int(fps*start_time)
    end_frame_id = int(fps*end_time)

    count = start_frame_id
  
    while success and count<=end_frame_id:

        # set reading position to the wanted frame 
        vidcap.set(cv.CAP_PROP_POS_FRAMES, count)
        success,image = vidcap.read()

        # save frame as JPEG file
        cv.imwrite("frame%d.jpg" % count, image) 

        count += 1

# get frames from 0.0 to 0.5 sec
get_frames(0.0,0.5)

# get frames from 3.0 to 3.5 sec
get_frames(3.0,3.5)

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