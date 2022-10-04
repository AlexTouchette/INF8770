# Algorithm arithmétique provenant du cours INF8770 Technologie Multimédia
# https://github.com/gabilodeau/INF8770/blob/master/Codage%20arithmetique.ipynb

import numpy as np



fileName="Codage_Predictif/textes/ABC.txt"
#fileName="Codage_Predictif/textes/randomText.txt"
#fileName="Codage_Predictif/textes/BeeMovieScript.txt"
file = open(fileName)

message = file.read()
SymbACoder = 6

ProbSymb =[[message[0], message.count(message[0])/len(message)]]
nbsymboles = 1

for i in range(1,len(message)):
    if not list(filter(lambda x: x[0] == message[i], ProbSymb)):
        ProbSymb += [[message[i], ProbSymb[-1][1]+message.count(message[i])/len(message)]]
        nbsymboles += 1
        
longueurOriginale = np.ceil(np.log2(nbsymboles))*SymbACoder 

Code = ProbSymb[:]
Code = [['', 0]] + ProbSymb[:]

for i in range(SymbACoder): 
    #Cherche dans quel intervalle est le symbole à coder
    temp = list(filter(lambda x: x[0] == message[i], Code))
    indice = Code.index(temp[0])

    #Calcul des bornes pour coder le caractère
    Debut = Code[indice-1][1]
    Plage = Code[indice][1] - Debut
    print(message[i], ' est dans l\'intervalle', indice, ' de ', Debut, ' à ', Debut + Plage)
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

    print(''.join(code))    
    
    #Décalage du séparateur décimal selon la puissance    
    for i in range(0,puissance):
        temp = code[indice-i-1];
        code[indice-i-1] = code[indice-i]
        code[indice-i] = temp
     
    print(''.join(code))
    
    #Enlève les zéros de trop et la partie avant le séparateur décimal
    
    ind = code.index('.')+1
    code = code[ind:]
    ind= code[::-1].index('1')
    code = code[:(len(code)-ind)]   
    codebinaire = ''.join(code)

    return codebinaire

messagecode = float_dec2bin(valfinale) #Essayer d'autres valeurs qui tombent dans l'intervalle
print(messagecode)

longueur = len(messagecode)
print("Longueur = {0}".format(longueur))
print("Longueur originale = {0}".format(longueurOriginale))