import numpy as np
import matplotlib.pyplot as py

def rgb2gray(rgb):
    return np.dot(rgb[:,:], [0.299, 0.587, 0.114])

fig1 = py.figure(figsize = (10,10))
imagelue = py.imread('Codage_Predictif\Images\pluton.jpg')
image=imagelue.astype('float')
image=rgb2gray(image)
py.imsave("Codage_Predictif\Images\pluton_gray.jpg",image,cmap = py.get_cmap('gray'))

matpred = [[0.33,0.33],[0.33,0.0]]


ProbSymb =[[image[0], image.count(image[0])/len(image)]]
nbsymboles = 1
SymbACoder = 6

for i in range(1,len(image)-2):
    for j in range(1,len(image[0])-2):
        if not list(filter(lambda x: x[0] == image[i][j], ProbSymb)):
            ProbSymb += [[image[i][j], ProbSymb[-1][1]+image.count(image[i][j])/len(image)]]
            nbsymboles += 1

longueurOriginale = np.ceil(np.log2(nbsymboles))*SymbACoder 


print(ProbSymb)