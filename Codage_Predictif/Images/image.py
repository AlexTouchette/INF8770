import numpy as np
import matplotlib.pyplot as py

def rgb2gray(rgb):
    return np.dot(rgb[:,:], [0.299, 0.587, 0.114])

#On transforme l'image en noir et blanc
fig1 = py.figure(figsize = (10,10))
imagelue = py.imread('test.jpg')
image=imagelue.astype('float')
image=rgb2gray(image)
py.imsave("test_gray.jpg",image,cmap = py.get_cmap('gray'))

matpred = [[0.33,0.33],[0.33,0.0]]

#On encode l'erreur sur la prédiction
imagepred = np.zeros((len(image)-2,len(image[0])-2))
for i in range(1,len(image)-2):
    for j in range(1,len(image[0])-2):
        imagepred[i][j]=image[i-1][j-1]*matpred[0][0]+image[i-1][j]*matpred[0][1]+image[i][j-1]*matpred[1][0]

#On enregistre l'image compressée
py.imsave("test_gray_compressed.jpg",imagepred,cmap = py.get_cmap('gray'))
      