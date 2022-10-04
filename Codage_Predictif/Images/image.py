import numpy as np
import matplotlib.pyplot as py

def rgb2gray(rgb):
    return np.dot(rgb[:,:], [0.299, 0.587, 0.114])

fig1 = py.figure(figsize = (10,10))
imagelue = py.imread('Codage_Predictif\Images\pluton.jpg')
image=imagelue.astype('float')
image=rgb2gray(image)
py.imsave("Codage_Predictif\Images\pluton_gray.jpg",image,cmap = py.get_cmap('gray'))


''' col=image[:,0]
image = np.column_stack((col,image))
col=image[:,len(image[0])-1]
image = np.column_stack((col,image))
row=image[0,:]
image = np.row_stack((row,image))
row=image[len(image)-1,:]
image = np.row_stack((row,image))
 '''
matpred = [[0.33,0.33],[0.33,0.0]]

#erreur = np.zeros((len(image)-2,len(image[0])-2))
imagepred = np.zeros((len(image)-2,len(image[0])-2))
for i in range(1,len(image)-2):
    for j in range(1,len(image[0])-2):
        imagepred[i][j]=image[i-1][j-1]*matpred[0][0]+image[i-1][j]*matpred[0][1]+image[i][j-1]*matpred[1][0]
        #erreur[i][j]=imagepred[i][j]-image[i][j]

py.imsave("Codage_Predictif\Images\pluton_gray_compressed.jpg",imagepred,cmap = py.get_cmap('gray'))
      