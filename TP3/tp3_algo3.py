import cv2 
import numpy as np 
from operator import itemgetter
import time

names = ["banane","plancheneige","planchesurf","pomme","tasse","zebre"]
reference_meds_b = []
reference_meds_g = []
reference_meds_r = []

req_meds_b = []
req_meds_g = []
req_meds_r = []

req_types = []


def plot_histogram(img):

    #get blue histogram
    img_copy = np.copy(img)
    img_copy[:,:,1] = 0
    img_copy[:,:,2] = 0
    hist_B, bins_b = np.histogram(img_copy, np.arange(256))
    
    #get green histogram
    img_copy = np.copy(img)
    img_copy[:,:,0] = 0
    img_copy[:,:,2] = 0
    hist_G, bins_b = np.histogram(img_copy, np.arange(256))

    #get red histogram
    img_copy = np.copy(img)
    img_copy[:,:,0] = 0
    img_copy[:,:,1] = 0
    hist_R, bins_R = np.histogram(img_copy, np.arange(256))
    return hist_B, hist_G, hist_R
        
def Read_db_images(folder, name, index):
    img = cv2.imread("{0}/{1}_{2}.png".format(folder, name,index))
    #width, height, chanels = img.shape
    #cropped_image = img[int((width/2)-100):int((width/2)+100), int((height/2)-100):int((height/2)+100)]
    return img

def get_type(index):
    if index >= 0 and index < 5:
        return names[0]
    if index >= 5 and index < 10:
        return names[1]
    if index >= 10 and index < 15:
        return names[2]
    if index >= 15 and index < 20:
        return names[3]
    if index >= 20 and index < 25:
        return names[4]
    if index >= 25 and index < 30:
        return names[5]

def get_best_type(diffs):
    smallest_diff = None
    if diffs[0] < diffs[1] and diffs[0] < diffs[2]:
        smallest_diff = diffs[0]
    elif diffs[1] < diffs[0] and diffs[1] < diffs[2]:
        smallest_diff = diffs[1]
    else:
        smallest_diff = diffs[2]
    return smallest_diff

if __name__ == "__main__":
    start = time.time()

    reference_images = []
    request_images = []

    #We read and crop the pictures
    for name in names:
        for i in range(1,6):
                reference_images.append(Read_db_images("banque_images", name, i))
    
    #We get the images histograms and calculate their medians
    for i in range(30):
        b, g, r = plot_histogram(reference_images[i])
        reference_meds_b.append(np.median(b))
        reference_meds_g.append(np.median(g))
        reference_meds_r.append(np.median(r))

    #We read the request images
    for i in range (1,9):
        request_images.append(Read_db_images("images_requete", "requete", i))

    #We get the request images histograms and calculate their medians and then identify them
    for i in range(len(request_images)):
        b, g, r = plot_histogram(request_images[i])
        req_meds_b.append(np.median(b))
        req_meds_g.append(np.median(g))
        req_meds_r.append(np.median(r))
        diffs_b = np.inf
        diffs_g = np.inf
        diffs_r = np.inf
        index_b = None
        index_g = None
        index_r = None
        types = []
        for j in range(30):
            temp_diff_b = abs(req_meds_b[i] - reference_meds_b[j])
            temp_diff_g = abs(req_meds_g[i] - reference_meds_g[j])
            temp_diff_r = abs(req_meds_r[i] - reference_meds_r[j])
            if temp_diff_b <= diffs_b:
                diffs_b = temp_diff_b
                index_b = j
            if temp_diff_g <= diffs_g:
                diffs_g = temp_diff_g
                index_g = j
            if temp_diff_r <= diffs_r:
                diffs_r = temp_diff_r
                index_r = j

        types.append(get_type(index_b))
        types.append(get_type(index_g))
        types.append(get_type(index_r))
        best_type = get_best_type([diffs_b, diffs_g, diffs_r])
        if best_type == diffs_b:
            types.append(get_type(index_b))   
        if best_type == diffs_g:
            types.append(get_type(index_g))   
        if best_type == diffs_r:
            types.append(get_type(index_r))   
        print(types)

    end = time.time()
    print(end - start)

    #Debug to see image
    #img = cv2.imread("banque_images/pomme_2.png")
    #cv2.imshow("img", img)
    #cv2.waitKey(0)

