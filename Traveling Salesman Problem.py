# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:51:51 2020

@author: As
"""
from random import shuffle
import random
from math import *

# ----------------- INITIALISATIONS -----------------
goal = 3450 #distance max que l'on veut parcourir

# Distances

N = 15 #nombre de villes
N_cell = N*N #nb cases tableau

d = [[0 for _ in range(N)] for _ in range(N)] #crée la matrice et la remplit de 0

c = 100 #créer des distances
for i in range (N) :
    for j in range (N) :
        c += 1
        d[i][j] = d[j][i]
        if i != j : #remplit les distances sauf la diagonale
            d[i][j] = c 
            d[j][i] = d[i][j]
            
# Individus 
In = 100 #nombre d'individus
Ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] 

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
En = 10 #nombre d'individus faisant partie de l'élite (les 10 meilleurs pour la fitness)

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
affiche_distance(d)
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
                fitness += d[n][p]
        fitness += d[Pop[i][N-1]][Pop[i][0]]
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
        
        