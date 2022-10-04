# Algorithm arithmétique provenant du cours INF8770 Technologie Multimédia
# https://github.com/gabilodeau/INF8770/blob/master/Codage%20arithmetique.ipynb

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

SymbACoder = 6

#Fonction qui compte le nombre répétition d'un même symboles 
def countSymbol(symbolI, symbolJ):
    count = 0
    for i in range(1,len(image)-2):
        for j in range(1,len(image[0])-2):
            if image[i][j] == image[symbolI][symbolJ]:
                count += 1
    return count

#On calcul la taille de l'image sur une dimension
size = 0
for i in range(1,len(image)-2):
    for j in range(1,len(image[0])-2):
        size += 1

count = countSymbol(0, 0)

ProbSymb =[[image[0][0], count/size]]
symbols = []
nbsymboles = 1

#On itère au travers de la liste pour calculer les probabilité de chaque symboles
for i in range(1,len(image)):
    for j in range(1, len(image)):
        if not list(filter(lambda x: x[0] == image[i][j], ProbSymb)):
            ProbSymb += [[image[i][j], ProbSymb[-1][1]+(countSymbol(i, j))/size]]
            symbols.append(image[i][j])
            nbsymboles += 1
        
longueurOriginale = np.ceil(np.log2(nbsymboles))*SymbACoder 

#On encode l'image en utilisant la liste symbols qui contient l'information de l'image sur une dimension
Code = ProbSymb[:]
Code = [['', 0]] + ProbSymb[:]
for i in range(SymbACoder): 
    #Cherche dans quel intervalle est le symbole à coder
    temp = list(filter(lambda x: x[0] == symbols[i], Code))
    indice = Code.index(temp[0])

    #Calcul des bornes pour coder le caractère
    Debut = Code[indice-1][1]
    Plage = Code[indice][1] - Debut
    print(symbols[i], ' est dans l\'intervalle', indice, ' de ', Debut, ' à ', Debut + Plage)
    print()      
    #Nouveaux intervalles pour coder le prochain symbole
    Code = [['', Debut]]  
    for j in range(len(ProbSymb)):
        Code += [[ProbSymb[j][0], Debut+ProbSymb[j][1]*Plage]]

ok = True
valfinale = 0
valEnBits = list('')
p = 0
while ok:
    p += 1
    #Essayer différentes sommes de puissance négative de 2
    valfinale += np.power(2.0,-p)
    valEnBits += '1' 
    if valfinale >= (Debut + Plage):
        valfinale -= np.power(2.0,-p) #Hors de la borne maximale, on annule l'ajout.
        valEnBits[-1] ='0'
    elif valfinale >= Debut :
        ok = False

print(valfinale)
print("".join(valEnBits))


#Table hex vers binaire
hex2bin = dict('{:x} {:04b}'.format(x,x).split() for x in range(16))

def float_dec2bin(d):
    
    #Note: je ne suis pas sûr que cela fonctionne toujours... J'ai fait un nombre de tests limité.
    
    hx = float(d).hex() #Conversion float vers hex
    p = hx.index('p')
    #Conversion hex vers bin avec la table
    bn = ''.join(hex2bin.get(char, char) for char in hx[2:p])
    code = list(bn)
    indice = code.index('.') # position du séparateur des décimales
    puissance = int(hx[p+2:]) # Décalage
    if puissance >= indice:
        #On ajoute des zéros pour pouvoir décaler le séparateur des décimales.
        zerosdeplus = "0" * (puissance-indice+1)
        bn = zerosdeplus + bn
        code = list(bn)
        indice = code.index('.') # nouvelle position du séparateur des décimales
    
    #Décalage du séparateur décimal selon la puissance    
    for i in range(0,puissance):
        temp = code[indice-i-1];
        code[indice-i-1] = code[indice-i]
        code[indice-i] = temp
     
    
    #Enlève les zéros de trop et la partie avant le séparateur décimal
    
    ind = code.index('.')+1
    code = code[ind:]
    ind= code[::-1].index('1')
    code = code[:(len(code)-ind)]   
    codebinaire = ''.join(code)

    return codebinaire

messagecode = float_dec2bin(valfinale) #Essayer d'autres valeurs qui tombent dans l'intervalle

longueur = len(messagecode)
print("Longueur = {0}".format(longueur))
print("Longueur originale = {0}".format(longueurOriginale))

