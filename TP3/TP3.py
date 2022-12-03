import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['image.cmap'] = 'gray' # Choix de la color map par défaut, ne pas modifier
import matplotlib
matplotlib.rcParams['figure.figsize'] = (15.0, 10.0) # Default figure size, you can modify this if you need to.
import cv2

cats  = ["banane","plancheneige","planchesurf","pomme","tasse","zebre"]

def plot_histogram(img):
    hist_B = cv2.calcHist(img, channels=[0],mask=None, histSize=[256], ranges=[0, 256])
    hist_G = cv2.calcHist(img, channels=[1],mask=None, histSize=[256], ranges=[0, 256])
    hist_R = cv2.calcHist(img, channels=[2],mask=None, histSize=[256], ranges=[0, 256])
    return hist_B, hist_G, hist_R


def Read_db_images(name, index):
    img = cv2.imread("TP3/banque_images/{0}_{1}.png".format(name,index))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def Distance_Euclidienne(hist_req, hist_comp):
    result=0
    for req, comp in zip(hist_req,hist_comp):
        result+=np.linalg.norm(req-comp)
    return result


for i in range (1, 9):
    print()
    print("IMAGE REQ  ",i)
    print()
    img = cv2.imread("TP3/images_requete/requete_%d.png" % (i))
    img_req = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist_req_B, hist_req_G, hist_req_R = plot_histogram(img_req)

    for cat in cats :
        for num in range(1,6):
            print("IMAGE DB",cat,num )
            img_comp = Read_db_images(cat, num)
            hist_comp_B, hist_comp_G, hist_comp_R = plot_histogram(img_comp)
            result_B = Distance_Euclidienne(hist_req_B,hist_comp_B)
            result_G = Distance_Euclidienne(hist_req_G,hist_comp_G)
            result_R= Distance_Euclidienne(hist_req_R,hist_comp_R)
            print(result_B,result_G,result_R)


        