import numpy as np
#import matplotlib.pyplot as plt
#plt.rcParams['image.cmap'] = 'gray' # Choix de la color map par défaut, ne pas modifier
#import matplotlib
#matplotlib.rcParams['figure.figsize'] = (15.0, 10.0) # Default figure size, you can modify this if you need to.
import cv2

cats  = ["banane","plancheneige","planchesurf","pomme","tasse","zebre"]

def plot_histogram(img):
    hist_B = cv2.calcHist(img, channels=[0],mask=None, histSize=[256], ranges=[0, 256])
    hist_G = cv2.calcHist(img, channels=[1],mask=None, histSize=[256], ranges=[0, 256])
    hist_R = cv2.calcHist(img, channels=[2],mask=None, histSize=[256], ranges=[0, 256])
    return hist_B, hist_G, hist_R


def Read_db_images(name, index):
    img = cv2.imread("banque_images/{0}_{1}.png".format(name,index))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # will have to resize image
    #img_rgb = cv2.resize(img_rgb, (h,w))

    return img_rgb

############ algo 1 ##################

def Distance_Euclidienne(hist_req, hist_comp):
    result=0
    for req, comp in zip(hist_req,hist_comp):
        result+=np.linalg.norm(req-comp)
    return result

def get_type(index):
    if index >= 0 and index < 5:
        return cats[0]
    if index >= 5 and index < 10:
        return cats[1]
    if index >= 10 and index < 15:
        return cats[2]
    if index >= 15 and index < 20:
        return cats[3]
    if index >= 20 and index < 25:
        return cats[4]
    if index >= 25 and index < 30:
        return cats[5]


for i in range (1, 9):
    print()
    print("IMAGE REQ  ",i)
    print()
    img = cv2.imread("images_requete/requete_%d.png" % (i))
    img_req = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist_req_B, hist_req_G, hist_req_R = plot_histogram(img_req)

    results = []

    for cat in cats :
        for num in range(1,6):
            img_comp = Read_db_images(cat, num)
            hist_comp_B, hist_comp_G, hist_comp_R = plot_histogram(img_comp)
            result_B = Distance_Euclidienne(hist_req_B,hist_comp_B)
            result_G = Distance_Euclidienne(hist_req_G,hist_comp_G)
            result_R= Distance_Euclidienne(hist_req_R,hist_comp_R)
        
            results.append((result_B + result_G + result_R)/3)
    
    #We get the best result:
    best_result = np.Inf
    second_result = np.Inf
    third_result = np.Inf
    index_best_result = None
    index_second_result = None
    index_third_result = None
    for j in range(30):
        if results[j] < best_result:
            third_result = second_result
            index_third_result = index_second_result
            second_result = best_result
            index_second_result = index_best_result
            best_result = results[j]
            index_best_result = j
        elif results[j] >= best_result and results[j] < second_result:
            third_result = second_result
            index_third_result = index_second_result
            second_result = results[j]
            index_second_result = j
        elif results[j] >= second_result and results[j] < third_result:
            third_result = results[j]
            index_third_result = j

    first_type = get_type(index_best_result)
    second_type = get_type(index_second_result)
    thrid_type = get_type(index_third_result)

    print("Best type is: ", first_type, " [", best_result, "] ")
    print("Second type is: ", second_type, " [", second_result, "] ")
    print("Third type is: ", thrid_type, " [", third_result, "] ")
    

############ algo 2 ##################

        