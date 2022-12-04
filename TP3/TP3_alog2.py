import cv2 
import numpy as np 
from operator import itemgetter

h = 900
w = 500
cats  = ["banane","plancheneige","planchesurf","pomme","tasse","zebre"]
#cats = ["pomme"]

def Read_db_images(name, index):
    img = cv2.imread("TP3/banque_images/{0}_{1}.png".format(name,index),cv2.IMREAD_GRAYSCALE)
    #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_res = cv2.resize(img, (h,w))
    # cv2.imshow("test",img_res)
    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows()
    return img_res

def get_filter():
    dim = h*w
    filter_ = [-1]* dim
    for i in range(h):
        for j in range(0,w,2):
            filter_[w*i+j] = 1  
    return filter_

def get_sum_convolution(img):
    img=img/255
    img_flatten = img.flatten()
    fil = get_filter()
    convolution = img_flatten*fil
    sum_conv = sum(convolution)
    return sum_conv

def get_best_matches(dic,n):
    best_matches = dict(sorted(dic.items(), key = itemgetter(1))[:n]) 
    return best_matches
           
        
        
    
dic ={}
for i in range (1, 9):
    print()
    print("IMAGE REQ  ",i)
    print()
    img_req = cv2.imread("TP3/images_requete/requete_%d.png" % (i) ,cv2.IMREAD_GRAYSCALE) 
    #img_req = cv2.imread("TP3/images_requete/requete_1.png" ,cv2.IMREAD_GRAYSCALE) 
    img_req_res = cv2.resize(img_req, (h,w))
    sum_conv_req = get_sum_convolution(img_req_res) 
    for cat in cats :
        for num in range(1,6):
            
            # print("IMAGE DB",cat,num )
            # print("req sum",sum_conv_req)

            img_bd = Read_db_images(cat, num)  
            sum_conv_bd = get_sum_convolution(img_bd)
            #print("Sum of Convolution: ",sum_conv_bd)
            diff = abs(sum_conv_req-sum_conv_bd)
            #print("diff",diff)
            
            key = "{0}_{1}".format(cat,num)
            dic[key] = diff 

    print(get_best_matches(dic,3))        

