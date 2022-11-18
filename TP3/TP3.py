import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['image.cmap'] = 'gray' # Choix de la color map par défaut, ne pas modifier
import matplotlib
matplotlib.rcParams['figure.figsize'] = (15.0, 10.0) # Default figure size, you can modify this if you need to.
import cv2

def plot_histogram(img):
    hist_B = cv2.calcHist(img, channels=[0],mask=None, histSize=[256], ranges=[0, 256])
    hist_G = cv2.calcHist(img, channels=[1],mask=None, histSize=[256], ranges=[0, 256])
    hist_R = cv2.calcHist(img, channels=[2],mask=None, histSize=[256], ranges=[0, 256])
    return hist_B, hist_G, hist_R

def Read_Bananes(index):
    img = cv2.imread("banque_images/banane_%d.png" % (index + 1))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def Read_Plancheneige(index):
    img = cv2.imread("banque_images/plancheneige_%d.png" % (index - 4))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def Read_Planchesurf(index):
    img = cv2.imread("banque_images/planchesurf_%d.png" % (index - 9))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def Read_Pomme(index):
    img = cv2.imread("banque_images/pomme_%d.png" % (index - 14))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def Read_Tasse(index):
    img = cv2.imread("banque_images/tasse_%d.png" % (index - 19))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def Read_Zebre(index):
    img = cv2.imread("banque_images/zebre_%d.png" % (index - 24))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def Distance_Euclidienne(hist_req, hist_comp):
    result=0
    for req, comp in zip(hist_req,hist_comp):
        result+=np.linalg.norm(req-comp)
    return result


for i in range (0, 7):
    img = cv2.imread("images_requete/requete_%d.png" % (i + 1))
    img_req = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist_req_B, hist_req_G, hist_req_R = plot_histogram(img_req)
    for j in range (0, 29):
        if (j >= 0 and j < 5 ):
            img_comp = Read_Bananes(j)
        """
        elif (j >= 5 and j < 10):
            img_comp = Read_Plancheneige(j)
        elif (j >= 10 and j < 15):
            img_comp = Read_Planchesurf(j)
        elif (j >= 15 and j < 20):
            img_comp = Read_Pomme(j)
        elif (j >= 20 and j < 25):
            img_comp = Read_Tasse(j)
        elif (j >= 25):
            img_comp = Read_Zebre(j)
        """
        hist_comp_B, hist_comp_G, hist_comp_R = plot_histogram(img_comp)


        