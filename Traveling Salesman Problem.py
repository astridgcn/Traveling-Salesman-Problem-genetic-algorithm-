# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 21:28:54 2022

@author: As
"""

# Remarques :
# - Ce code n'est pas le plus optimisé, mais il est suffisamment simple pour illustrer le principe de l'algorithme.
# - Ne gère par les erreurs d'input (variables initialement initialisées directement dans le code) : 
#       Saisie de texte au lieu de nombres.
#       Nombres incohérents (du style créer 20 villes avec minimum 100km entre chaque et vouloir parcourir uniquement 100km).
#       Etc.
# - Pourrait proposer de créer une fonction qui prend en entrée une liste de villes et qui renvoie une liste de distances.
# - Ne gère pas le programme qui tourne en boucle (distance à atteindre trop petite par rapport aux distances).
# - On pourrait proposer une distance maximale en fonction des distances générées par exemple.

# N'hésitez pas à proposer des améliorations et/ou extensions !

# ----------------- LIBRAIRIES -----------------

from random import shuffle
import random
from math import *

# ----------------- INITIALISATIONS -----------------
print("Distance maximale que vous souhaitez parcourir : ")
goal = int(input())
# goal = 3400

# Distances entre les villes
print("Nombre de villes que vous souhaitez visiter : ")
N = int(input())
# N = 15
N_cell = N*N #Nombre cases tableau

dist = [[0 for _ in range(N)] for _ in range(N)] #crée la matrice et la remplit de 0

print("Distance minimale entre les villes que vous souhaitez créer : ")
c = int(input())
# c = 100
for i in range (N) :
    for j in range (N) :
        c += 1
        dist[i][j] = dist[j][i]
        if i != j : #remplit les distances sauf la diagonale
            dist[i][j] = c 
            dist[j][i] = dist[i][j]
            
# Individus 
print("Nombre d'individus dans chaque génération : ")
In = int(input()) #nombre d'individus
# In = 100
Ind = list(range(0,N)) #individu parcourant les n villes dans l'ordre
# Ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] 
# Population
Pop = []
   
for i in range (In) :
    naissance = Ind[:]
    shuffle(naissance)
    Pop.append(naissance)
    
# Nouvelle population
NewPop = [[0 for _ in range(N)] for _ in range(In)]

# Fitness
Fitness = [[0 for _ in range(2)] for _ in range(In)] #liste avec indice individu et sa fitness (inutile car on a l'indice avec i mais utile quand on ordonne)
print("Nombre d'individus à conserver : ")
En = int(input()) #nombre d'individus faisant partie de l'élite (les meilleurs pour la fitness)
# En = 10

# ----------------- FONCTIONS -----------------
def affiche_distance (liste) :
    print ("\nTableau des distances : \n")
    print ("    ", end="")
    for k in range (N) :
        print ("", chr(k + 65), " ", end="")
    print ("")
    print ("    -----------------------------------------------------------")
    for i in range (N) :
        print (chr (i + 65)," ", end="")
        print ("| ", end="")
        for j in range (N):        
            print (liste[i][j], end=" ")
        print ("|")
    print ("    -----------------------------------------------------------\n")
    
def affiche_individu (liste) :
    print ("\nListe des individus : \n")
    for k in range (In) :
        print (Pop[k])
    print("\n")  
    
# ----------------- DEBUT -----------------
affiche_distance(dist)
affiche_individu(Pop)

g = 0 #nb génération
min = 100000 #minimum élevé pour être sûr qu'il soit battu
while min >= goal :
    print ("\n-------------------- Génération", g, "-------------------")
    if g != 0 :
        print ("Distance minimale de la dernière génération :", min)
    Fitness = [[0 for _ in range(2)] for _ in range(In)]
    print ("\n---------------------- Fitness ----------------------")
    
    # Calcul de la fitness des chemins
    
    for i in range (In) : #pour chaque individu
        fitness = 0 
        n = 0 #pour simplifier l'écriture et vérifier les valeurs
        p = 0
        for j in range (N) : #pour 15 villes
            if j!= N-1 :
                n = Pop[i][j] 
                p = Pop[i][j+1]
                fitness += dist[n][p]
        fitness += dist[Pop[i][N-1]][Pop[i][0]]
        Fitness[i][0] = fitness
        Fitness[i][1] = i
        #print ("Fitness individu", i, " : ", fitness) 
        
    Fitness.sort()
    #print ("\n", Fitness) #utiliser fonction psq c moche
    FElite = Fitness [0:En:1] #Fitness de l'élite
    min = FElite[0][0]
    best = FElite[0][1]
    print ("\nFitness et indice des 10 meilleurs individus :")
    print(FElite)
    #print ("Min :",min)
    
    print ("\n-------------------- Croisements --------------------")
    
    
    for i in range (In-En) : #on va créer 90 nouveaux individus
        #print ("\nNouvel individu", i)
        # Parent 1
        P1 = random.randint(1, En) #un chiffre aléatoire entre 1 et 10
        #print ("P1 :", P1)
        n1 = FElite[P1-1][1] #indice du parent 1
        #print ("Parent 1 :", n1)
        
        # Troncature 
        t = random.randint(1, N) #indice pour la troncature
        #print ("Endroit de la coupure :", t)
        
        # On prend les t gènes du Parent 1
        for j in range (t) : 
            x = Pop[n1][j]
            NewPop[i][j] = x
        #print(NewPop[i])
    
        # Parent 2
        P2 = random.randint(1, En) #un chiffre aléatoire entre 1 et 10
        while P1 == P2 : #éviter la reproduction avec lui-même
            P2 = random.randint(1, En)
        #print ("P2 :", P2)
        n2 = FElite[P2-1][1]
        #print ("Parent 2 :", n2)
        
        # On prend les autres chez le Parent 2
        v = N - t#nb gènes
        #print("v :", v)
        for k in range (v) : 
            w = k + t
            #print("w :", w)
            for n in range (N) : 
                if Pop[n2][n] not in (NewPop[i]) :
                    x = Pop[n2][n]
                    NewPop[i][w] = x
        #print (NewPop[i])
        
    # On ajoute les En parents à la nouvelle population
    for i in range (En) :
        #print ("\nIndividu", i+90)
        n = FElite[i][1]
        NewPop[i+90] = Pop[n][:]
        #print(NewPop[i])
    
    print("Nouvelle génération", g, "crée.")
    
    #Un des best de la gen (un de bests car plusieurs chemins peuvent faire la même fitness)
    winner = Pop[best][:]
    
    # Nouvelle génération
    g += 1
    
    # La nouvelle population NewPop devient Pop
    Pop = NewPop[:]
    #print(Pop)
    
    # NewPop est mise à 0
    NewPop = [[0 for _ in range(N)] for _ in range(In)]
    #print (NewPop)

print ("\n--------------------- Réussite ----------------------")
print ("\nGoal atteint au bout de", g, "générations.")
print ("Le premier chemin trouvé pour parcourir", goal, "km est :")
print (winner)
        
        
