# Première étape: Division de la trame en macroblocs --------------------
import numpy as np

# On génère une image aléatoire pour l'instant, on va utiliser les trames
# du vidéo quand on aura le vidéo

grey_levels = 256
test_image = np.random.randint(0,grey_levels, size=(32, 32))

# On définit la largeur et la hauteur des macroblocs
largeur = 16
hauteur = 16

windows = []


# On découpe l'image en macroblocs
for l in range(0,test_image.shape[0], largeur):
    for h in range(0,test_image.shape[1], hauteur):
        window = test_image[l:l+largeur,h:h+hauteur]
        hist = np.histogram(window,bins=grey_levels)
        windows.append(window)
        

# Deuxième étape: Estimation des vecteurs de mouvement ------------------


# Troisième étapes: Calcul des blocs de différences ---------------------

