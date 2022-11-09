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
#get_frames(0.0,0.5)

# get frames from 3.0 to 3.5 sec
#get_frames(3.0,3.5)

greyscale = 256
frames =[]
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

for i in range(15):
    frame = cv.imread("TP2/FrameSeq1/frame%d.jpg" % i) 
    frames.append(frame)
   
def compare_macroblocks(index,x,y):
    h = frames[index].shape[0]
    w = frames[index].shape[1]
    
    #on commence par comparer avec le marcobloc de la trame t-1 à la meme position 
    # DMaMb1 = frames[index][x:x+16, y:y+16] - frames[index-1][x:x+16, y:y+16]
    # result1 = sum(DMaMb1[0][0])
    # print("result1",result1)
    # if result1==0:return (0,0) 
    
    for vx in range(-4,4):
        for vy in range(-4,4):
            if((x+16+vx<w and y+16+vy<h)and (x+vx>0 and y+vy>0)):
                DMaMb = frames[index][x:x+16, y:y+16] - frames[index-1][x+vx:x+16+vx, y+vy:y+16+vy]
                result = sum(DMaMb[vx][vx])
                print('result',result)
                #print(DMaMb)
                if result <800: 
                    return (vx,vy) 
                else:
                    print("X : ",x," Y : ",y)
                    #print(DMaMb)

#print(compare_macroblocks(1,0,1)) 

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
            print("vector",compare_macroblocks(index,x,y))


            # Définition du CPB (4:0:0):
            #J'ai mit 4 pour l'instant mais je suis vraiment pas certain
            imgYCC = 4

            # Définition des 4 blocs Y:
            b0 = image[x:x+deltaMoitier, y:y+deltaMoitier]                          # Coin supérieur gauche à milieu
            b1 = image[x+deltaMoitier:x+deltaPlein, y:y+deltaMoitier]               # Milieu haut à milieu droit
            b2 = image[x:x+deltaMoitier, y+deltaMoitier:y+deltaPlein]               # Milieu gauche à milieu bas
            b3 = image[x+deltaMoitier:x+deltaPlein, y+deltaMoitier:y+deltaPlein]    # Milieu à coin inférieur droit

            #print("block0",b0,"block1",b1,"block2",b2,"block3",b3)
            macroblock = Macroblock(macroAddrX, macroAddrY, macroType, imgYCC, b0, b1, b2, b3)
            macroblocks.append(macroblock)
    return macroblocks


        
        

#print(compare_macroblocks(1,0,0))
macroblocks = []



# for i in range(15):
#     frame = cv.imread("FrameSeq1/frame%d.jpg" % i)
#     macroblocks.append(get_macroblocks(frame, i))
#     #print(macroblocks[i][0])

get_macroblocks(frames[1], 1)



