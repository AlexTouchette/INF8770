# Première étape: Division de la trame en macroblocs --------------------
import numpy as np
import cv2 as cv

vidcap = cv.VideoCapture('bouncing_dvd_logo_1.mp4')
greyscale = 256


class Macroblock:
    #Doit ajouter vx, vy
    def __init__(self, x, y, type, CBP, b0, b1, b2, b3):
        self.x = x
        self.y = y
        self.type = type
        #self.vx = vx
        #self.vy = vy
        self.CBP = CBP
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
    


def get_frames():
    success,image = vidcap.read()
    count = 0
    while success:
        cv.imwrite("frame%d.jpg" % count, image) # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1

def get_macroblocks(image, index):
    # On définit les variation des macroblocs
    deltaPlein = 16
    deltaMoitier = 8

    macroblocks = []

    # On itère au travers de la trame pour isoler chaque macro bloc
    for x in range(0,image.shape[0], deltaPlein):
        for y in range(0,image.shape[1], deltaPlein):
            # Définition du macroblock de départ avec son adresse
            macroAddrX = x
            macroAddrY = y
            
            # Définition du type du macroblock:
            macroType = 'I' if index == 0 else 'P'


            # Définition du vx et vy:
            # Still need to figure that out lol


            # Définition du CPB (4:0:0):
            #J'ai mit 4 pour l'instant mais je suis vraiment pas certain
            imgYCC = 4

            # Définition des 4 blocs Y:
            b0 = image[x:x+deltaMoitier, y:y+deltaMoitier]                          # Coin supérieur gauche à milieu
            b1 = image[x+deltaMoitier:x+deltaPlein, y:y+deltaMoitier]               # Milieu haut à milieu droit
            b2 = image[x:x+deltaMoitier, y+deltaMoitier:y+deltaPlein]               # Milieu gauche à milieu bas
            b3 = image[x+deltaMoitier:x+deltaPlein, y+deltaMoitier:y+deltaPlein]    # Milieu à coin inférieur droit

            macroblock = Macroblock(macroAddrX, macroAddrY, macroType, imgYCC, b0, b1, b2, b3)
            macroblocks.append(macroblock)
    return macroblocks



macroblocks = []

for i in range(15):
    frame = cv.imread("FrameSeq1/frame%d.jpg" % i)
    macroblocks.append(get_macroblocks(frame, i))
    #print(macroblocks[i][0])



