# Première étape: Division de la trame en macroblocs --------------------
import numpy as np
import cv2 as cv


################################## GET FRAMES ####################################
def get_frames(start_time, end_time):
    
    success=True
    
    # read video 
    #vidcap = cv.VideoCapture('TP2/bouncing_dvd_logo_1.mp4') 
    #vidcap = cv.VideoCapture('TP2/test.mp4')
    vidcap = cv.VideoCapture('TP2/bouncing_ball.mp4') 

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
#get_frames(0.0,0.5)
#get_frames(7.0,7.5)

# get frames from 3.0 to 3.5 sec
#get_frames(3.0,3.5)


################################## Macrobblock class ####################################

class Macroblock:
    #Doit ajouter vx, vy
    def __init__(self, x, y, type, vx, vy, CBP, b0, b1, b2, b3):
        self.x = x
        self.y = y
        self.type = type
        self.vx = vx
        self.vy = vy
        self.CBP = CBP
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3

################################## GET MACROBLOCK VECTORS ####################################
def compare_macroblocks(index,x,y):
    
    # hauteur et largeur de l'image
    h = frames[index].shape[0]
    w = frames[index].shape[1]
    
    # calcul de l'erreur quadratique entre 
    # le marcoblock de la trame t et celui de la trame t-1 à la meme position
    diff_current = cv.subtract(frames[index][x:x+16, y:y+16],frames[index-1][x:x+16, y:y+16]) 
    err_current = np.sum(diff_current**2)
    mse_current = err_current/(float(h*w))
    
    min_mse = mse_current
    vector = (0,0)
    diff_block=diff_current 
    
    # déplace dans la trame t-1 dans un rayon de 6 pixels 
    for vx in range(-6,6):
        for vy in range(-6,6):
            
            # vérifier que la zone de recherche ne dépace pas l'hauteur et la largeur de la trame
            if((x+16+vx<w and y+16+vy<h)and (x+vx>0 and y+vy>0)):

                # vérifier que les deux marcoblock à comparer ont la meme taille 
                if len(frames[index][x:x+16, y:y+16]) == len(frames[index-1][x+vx:x+16+vx, y+vy:y+16+vy]) :
                    
                    # calcul de l'erreur quadratique 
                    diff = cv.subtract(frames[index][x:x+16, y:y+16],frames[index-1][x+vx:x+16+vx, y+vy:y+16+vy])
                    err = np.sum(diff**2)
                    mse = err/(float(h*w))
                    
                    # recherche du meilleur macroblock correcpendant
                    # (erreur quadratique la plus faible )
                    if mse < min_mse :
                        min_mse = mse
                        vector = (vx,vy)
                        diff_block = diff 
                       
                 
    return vector, diff_block


################################## CREATE MACROBLOCKS ####################################

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
            vector, diff_block = compare_macroblocks(index,x,y)
            
            vx = vector[0]
            vy = vector[1]

            # Définition des 4 blocs Y:
            b0 = diff_block[0:deltaMoitier, 0:deltaMoitier]                          # Coin supérieur gauche à milieu
            b1 = diff_block[deltaMoitier:deltaPlein, 0:deltaMoitier]               # Milieu haut à milieu droit
            b2 = diff_block[0:deltaMoitier, deltaMoitier:deltaPlein]               # Milieu gauche à milieu bas
            b3 = diff_block[deltaMoitier:deltaPlein, deltaMoitier:deltaPlein]    # Milieu à coin inférieur droit

            # Définition du CPB (4:0:0):
            #J'ai mit 4 pour l'instant mais je suis vraiment pas certain

            bit1 = 1 if all((element == [0,0,0]).all() for element in b0) else 0
            bit2 = 1 if all((element == [0,0,0]).all() for element in b1) else 0
            bit3 = 1 if all((element == [0,0,0]).all() for element in b2) else 0
            bit4 = 1 if all((element == [0,0,0]).all() for element in b3) else 0

            CBP = "b'{0}{1}{2}{3}'".format(bit1,bit2,bit3,bit4)
            
            #print("block0",b0,"block1",b1,"block2",b2,"block3",b3)
            macroblock = Macroblock(macroAddrX, macroAddrY, macroType,vx , vy, CBP, b0, b1, b2, b3)
            macroblocks.append(macroblock)
    return macroblocks

################################## CREATE FRAMES LISTE ####################################     
frames =[]
for i in range(210,225):
    #frame = cv.imread("TP2/FrameSeq1/frame%d.jpg" % i) 
    #frame = cv.imread("TP2/test/frame%d.jpg" % i) 
    frame = cv.imread("TP2/framesTest/frame%d.jpg" % i) 
    frames.append(frame)       

################################## MAIN ####################################   
macroblocks = []

# for i in range(15):
#     frame = cv.imread("FrameSeq1/frame%d.jpg" % i)
#     macroblocks.append(get_macroblocks(frame, i))
#     #print(macroblocks[i][0])

get_macroblocks(frames[1], 1)



