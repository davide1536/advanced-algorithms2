from Grafo import Grafo
from Nodo import Nodo
from Arco import Arco
from Utility import convert, calcEuclDist, calcGeoDist, prim, preOrderVisit, getTree, creaSottoinsiemi
from NodeSet import NodeSet
import random
import os
import math
from random import seed
from random import randint
import gc
from time import perf_counter_ns
from collections import defaultdict
import collections
import matplotlib.pyplot as plt
import copy
import time
import random


per_m = "algoritmi-avanzati-laboratorio2/"
#per_m = ""
directory = per_m+"tsp_dataset/"
lista_grafi = []



def parsing(directory):
    for file in os.listdir(directory):
            crea_grafi(file)


#funzione che dato un path, aggiunge un oggetto grafo 
#alla lista lista_grafi
def crea_grafi(path):

    global lista_grafi
    g = Grafo()
    
    lista_nodi = []
    id2Node = {}
    edge_weigt_format = None
    display_data_type = None

    f = open(directory + path, "r")

    #leggo la prima riga
    riga = f.readline().split(" ")
    
    fine = False
    while not fine :
        
        if riga[0] == "NAME:":
            name = riga[1]
            riga = f.readline().split(" ")      #cambio riga

        elif riga[0] == "NAME":                 #un paio di grafi hanno lo spazio prima di ":"
            name = riga[2]
            riga = f.readline().split(" ")      
        
        elif riga[0] == "TYPE:":
            g_type = riga[1] 
            riga = f.readline().split(" ")
        
        elif riga[0] == "TYPE":                 
            g_type = riga[2] 
            riga = f.readline().split(" ")
        
        elif riga[0] == "COMMENT:":
            comment = riga[1]
            riga = f.readline().split(" ")
        
        elif riga[0] == "COMMENT":
            comment = riga[2]
            riga = f.readline().split(" ")
        
        elif riga[0] == "DIMENSION:":
            n_nodi = int(riga[1])
            riga = f.readline().split(" ")
        
        elif riga[0] == "DIMENSION":
            n_nodi = int(riga[2])
            riga = f.readline().split(" ")
        
        elif riga[0] == "EDGE_WEIGHT_TYPE:":    
            edge_weigt_type = riga[1]
            riga = f.readline().split(" ")
        
        elif riga[0] == "EDGE_WEIGHT_TYPE":
            edge_weigt_type = riga[2]
            riga = f.readline().split(" ")
        
        elif riga[0] == "EDGE_WEIGHT_FORMAT:":
            edge_weigt_format = riga[1]
            riga = f.readline().split(" ")

        elif riga[0] == "DISPLAY_DATA_TYPE:":
            display_data_type = riga[1]
            riga = f.readline().split(" ")
        
        else:
            fine = True

    
    #inizio parse nodi
    #creo lista di stringhe "id_nodo, coord_x, coord_y"
    righe = f.read().splitlines()
    
    #divido le stringhe in liste di 3 valori [nodo1, nodo2, peso]
    lista_valori = []
    for riga in righe:
        value = riga.split()
        if len(value) != 1 and len(value) != 0:
            lista_valori.append(value)
        else:
            f.close()
    f.close()

    #creo i nodi, faccio le conversioni e li aggiungo alla lista nodi
    for riga in lista_valori:
        nodo = Nodo()
        nodo.id = int(riga[0])
        
        if edge_weigt_type == "GEO":
            #conversione 
            nodo.x = convert(float(riga[1]))
            nodo.y = convert(float(riga[1]))
        else:
            nodo.x = float(riga[1])
            nodo.y = float(riga[2])
        
        lista_nodi.append(nodo)
        id2Node[nodo.id] = nodo

    #inizializzo matrice di adiacenza
    adj_matrix = [[0]*(n_nodi+1) for i in range(n_nodi+1)]  
    
    #definisco anticipatamente id2Node per poterlo utilizzare subito
    g.id2Node = id2Node

    #calcolo le distanze
    for i in range(1, n_nodi+1):
        for j in range(1, n_nodi+1):
            if i != j:
                if edge_weigt_type == "GEO":
                    adj_matrix[i][j] = calcGeoDist(g.getNodo(i), g.getNodo(j))
                else:
                    adj_matrix[i][j] = calcEuclDist(g.getNodo(i), g.getNodo(j))
    

    g.n_nodi = n_nodi
    g.name = name
    g.g_type = g_type
    g.comment = comment
    g.edge_weigt_type = edge_weigt_type
    g.edge_weigt_format = edge_weigt_format
    g.display_data_type = display_data_type
    g.lista_nodi = lista_nodi
    g.lista_id_nodi = [n for n in range(1, n_nodi+1)]       #maybe inutile
    g.adj_matrix = adj_matrix
    

    lista_grafi.append(g)
    print("aggiunto grafo con", g.n_nodi, "nodi")



#algoritmo 2-approssimato
def approx_tsp_tour(g):
    h = []
    radice = random.choice(g.lista_nodi)
    prim(g, radice)
    getTree(g)
    h = preOrderVisit(radice)
    h.append(radice)
    hamiltonCycle = h
    return hamiltonCycle



#algoritmo esatto Held e Karp
def hkVisit(g,v,S):
    new_set_node = []
    if S == [v]:
        return g.adj_matrix[1][v]
    
    elif g.diz_pesi[g.getNodeSet(v,S)] != None:
        return g.diz_pesi[g.getNodeSet(v,S)]
    
    else:
        mindist = math.inf
        minprec = None
        new_set_node[:] = S
        #new_set_node.remove(v)
        new_set_node.pop(0)     #possibile miglioria
        for u in new_set_node:
            dist = hkVisit(g, u, new_set_node)
            #print(dist, g.adj_matrix[u][v])
            if dist + g.adj_matrix[u][v] < mindist:
                mindist = dist + g.adj_matrix[u][v]
                minprec = u
        g.diz_pesi[g.getNodeSet(v, S)] = mindist
        g.diz_padri[g.getNodeSet(v, S)] = minprec
        
        return mindist
    



#funzione per chiamare l'algorirmo Held e Karp
def hkTsp(g):
    #inizializzo le liste v,S
    creaSottoinsiemi(g)
    
    # aggiungo il vertice 0 (1 nel nostro caso)
    nodeSet = NodeSet()
    nodeSet.v = 1        
    nodeSet.S[:]= g.lista_id_nodi
    v = [1]
    v.append(g.lista_id_nodi)
    id_vS = str(v) 
    g.id2NodeSet[id_vS] = nodeSet

    g.diz_pesi[nodeSet] = None
    g.diz_padri[nodeSet] = 1
        
    
    return hkVisit(g, 1, g.lista_id_nodi)



######################## MAIN ########################
parsing(directory)

print("fine parsing")


for g in lista_grafi:
    if g.n_nodi == 8:
        #for i in g.lista_id_nodi:
        #    print(i, g.getNodo(i).x, g.getNodo(i).y)
        #for j in g.adj_matrix:
            #print(j)
        
        peso = hkTsp(g)
        print(peso)
        
        #for nodo in g.id2NodeSet.keys():
            #print("id:",nodo, "nodo:", g.id2NodeSet[nodo].v, "subset:", g.id2NodeSet[nodo].S)
        #print(len(g.id2NodeSet.keys()))

        # peso = hkTsp(g)
        #print(peso)
        
        #for i in g.diz_padri.keys():
            #print((i.v, i.S), g.diz_pesi[i])

        #for i in g.id2NodeSet.keys():
        #    print(i, g.id2NodeSet[i])


# for grafo in lista_grafi:
#     hamiltonCycle = approx_tsp_tour(grafo)

# for nodo in grafo.lista_nodi:
#     print(nodo.padre)
#     print(nodo.figlio)





