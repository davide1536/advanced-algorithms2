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


#per_m = "algoritmi-avanzati-laboratorio2/"
per_m = ""
directory = per_m+"tsp_dataset/"
lista_grafi = []

def computeWeight(c, g):
    pesoCiclo = 0
    for i,nodo in enumerate(c):
        if i != (len(c)-1): 
            nextNode = c[i+1]
            pesoCiclo += g.adj_matrix[nodo.id][nextNode.id]
            # print("nodo ", nodo.id, "vicino ", c[i+1].id)
            # print("peso ", g.adj_matrix[nodo.id][nextNode.id])

    return pesoCiclo


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
        
        if "GEO" in edge_weigt_type :
            #conversione 
            nodo.x = convert(float(riga[1]))
            nodo.y = convert(float(riga[2])) 
            
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
                if "GEO" in edge_weigt_type:
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
    #print("aggiunto grafo con", g.n_nodi, "nodi")




############################################### 2-APPROSSIMATO ###############################################



#algoritmo 2-approssimato
def approx_tsp_tour(g):
    h = []
    radice = random.choice(g.lista_nodi)
    #radice = g.lista_nodi[0]

    #print("la radice e'", radice.id)
    prim(g, radice)
    # print("il peso dell'albero e'", g.totPeso)
    # for j in g.lista_nodi:
    #     print ("sono ", j.id, "mio padre e'")
    #     if j.padre != None:
    #      print(j.padre.id)

    getTree(g)

    # for j in g.lista_nodi:
    #     print ("sono ", j.id, "i miei figli sono:")
    #     for i in j.figlio:
    #         print(i.id)

   

    h = preOrderVisit(radice, h)
    h.append(radice)
    hamiltonCycle = h
    return hamiltonCycle


############################################### HELD-KARP ###############################################

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
        new_set_node.remove(v)
        for u in new_set_node:
            dist = hkVisit(g, u, new_set_node)
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


############################################### CLOSEST_INSERTION ###############################################


def updateCiclo(nodoToExtract, ciclo, noCiclo, position):
    noCiclo.remove(nodoToExtract)
    ciclo.insert(position, nodoToExtract)


def getClosestNode(g, ciclo, noCiclo):
    minPeso = float('inf')
    for nodo1 in ciclo:
        for nodo2 in noCiclo:
            peso = g.adj_matrix[nodo1][nodo2]
            if peso < minPeso:
                minPeso = peso
                nodo_k = nodo2
    return nodo_k


def getPosition(g, k, ciclo, noCiclo):
    minPeso = float('inf')
    min_i = 1 #al primo ciclo del while restituisco il valore di default (1) in quanto nel circuito parziale è presente solo il primo elemento
    for i in ciclo:
        for j in ciclo:
            if i != j:
                pesoi_k = g.adj_matrix[i][k]
                pesok_j = g.adj_matrix[k][j]
                pesoi_j = g.adj_matrix[i][j]
                peso = pesoi_k + pesok_j - pesoi_j
                if peso < minPeso:
                    minPeso = peso
                    min_i = i
               
    return min_i, minPeso

  
def closest_insertion(g):
    #tengo traccia dei nodi nel circuito parziale attraverso queste 2 liste
    verticiNonCiclo = copy.deepcopy(g.lista_id_nodi) 
    circuitoParziale = [] #lista contenente il circuito parziale
    #radice = random.choice(g.lista_nodi)

    nodo_k = 1 #indico con nodo_k il nodo da inserire all'interno del circuito parziale
    updateCiclo(nodo_k, circuitoParziale, verticiNonCiclo,0)    
    while len(verticiNonCiclo) != 0: #finche non ho inserito tutti i vertici
        #if len(circuitoParziale) == 2:
        #    circuitoParziale.append(1)
        nodo_k = getClosestNode(g, circuitoParziale, verticiNonCiclo)
        node_i, min_peso = getPosition(g, nodo_k, circuitoParziale, verticiNonCiclo)
        g.totPeso += min_peso
        #print("circuito")
        #print([nodo for nodo in circuitoParziale])
        #print("nodo precedente", node_i, "nodo da aggiungere", nodo_k)
        position = circuitoParziale.index(node_i)
        updateCiclo(nodo_k, circuitoParziale, verticiNonCiclo, position+1)

    circuitoParziale.append(1)     
    return circuitoParziale
    

############################################### CLOSEST_INSERTION 2 ###############################################

#fuznione per trovare il vicino più vicino
def closest_neighbour2(g, circuito, no_circuito):
    min_peso = math.inf
    closest = None
    for nodo in circuito:
        for vicino in range(len(no_circuito)):
            peso = g.adj_matrix[nodo.id][no_circuito[vicino].id]
            if peso < min_peso:
                min_peso = peso
                closest = copy.deepcopy(no_circuito[vicino])
                index = vicino
    
    return closest, index


#versione rivista di closest_neighbour, da controllare meglio
def closest_neighbour(g, circuito, no_circuito):
    min_peso = [None, math.inf, 0]
    k = None    
    
    for vicino in range(len(no_circuito)):
        min_k = math.inf        #dato un k, non ancora inserito nel circuito, il suo peso è il minimo tra i pesi calcolati con ogni nodo del circuito
        for nodo in circuito:
            peso = g.adj_matrix[nodo.id][no_circuito[vicino].id]
            if peso < min_k:
                min_k = peso
                k = no_circuito[vicino]
                index = vicino

        if min_k < min_peso[1]:
            min_peso[1] = min_k
            min_peso[0] = k
            min_peso[2] = index
    
    return min_peso[0], min_peso[2]



def insert_closest(g, closest, circuito_parziale):
    min_dist = math.inf
    for i in range(len(circuito_parziale)):
        if i < len(circuito_parziale)-1:
            dist = ( g.adj_matrix[ circuito_parziale[i].id ][closest.id] + 
                     g.adj_matrix[closest.id][ circuito_parziale[i+1].id ] - 
                     g.adj_matrix[ circuito_parziale[i].id ][ circuito_parziale[i+1].id ] )
            if dist < min_dist:
                min_dist = dist
        else:
            dist2 = ( g.adj_matrix[ circuito_parziale[i].id ][closest.id] + 
                      g.adj_matrix[closest.id][ circuito_parziale[0].id ] - 
                      g.adj_matrix[ circuito_parziale[i].id ][ circuito_parziale[0].id ] )
            if dist2 < min_dist:
                circuito_parziale.append(closest)
                return
        
    circuito_parziale.insert(i+1, closest)


def remove_closest(index, no_circuito):
    no_circuito[index] = no_circuito[-1]
    no_circuito.pop()


def closest_insertion2(g):
    no_circuito = []                    #lista contentente i nodi non ancora inseriti nel circuito
    no_circuito[:] = g.lista_nodi[1:]   #lista nodi, escluso il primo
    
    circuito_parziale = [g.getNodo(1)]             #circuito parziale inizializzato con il primo nodo
    
    while len(no_circuito) != 0:
        closest, index = closest_neighbour(g, circuito_parziale, no_circuito)

        insert_closest(g, closest, circuito_parziale)
        remove_closest(index, no_circuito)
    
    circuito_parziale.append(g.getNodo(1))

    return circuito_parziale
    










################################################ MAIN ################################################

parsing(directory)

print("fine parsing")

lista_grafi = sorted(lista_grafi, key=lambda grafo: grafo.n_nodi)

#for g in lista_grafi:
    #if g.n_nodi == 14:
        #for i in g.lista_id_nodi:
        #   print(i, g.getNodo(i).x, g.getNodo(i).y)
        #for j in g.adj_matrix:
        #    print(j)
        #print("***********************************")
        #peso = hkTsp(g)
        #print(peso)
        #print("***********************************")
        #for nodo in g.id2NodeSet.keys():
            #print("id:",nodo, "nodo:", g.id2NodeSet[nodo].v, "subset:", g.id2NodeSet[nodo].S)
        #print(len(g.id2NodeSet.keys()))

        # peso = hkTsp(g)
        #print(peso)
        
        #for i in g.diz_padri.keys():
            #print((i.v, i.S), g.diz_pesi[i])

        #for i in g.id2NodeSet.keys():
        #    print(i, g.id2NodeSet[i])

sol_ottime = { 8 : 14,
               14 : 3323, 
               16 : 6859, 
               22 : 7013,
               51 : 426,
               52 : 7542,
               100 : 21294,
               #100 : 21282,
               150 : 6528,
               202 : 40160,
               229 : 134602,
               442 : 50778,
               493 : 35002,
               1000 : 18659688 }


for g in lista_grafi:
    if g.n_nodi == 8:
        print("grafo con: ", g.n_nodi, "nodi")

    #hamiltonCycle1 = approx_tsp_tour(g)
    #peso1 = computeWeight(hamiltonCycle1, g)
    
        hamiltonCycle2 = closest_insertion2(g)
        circ = [nodo.id for nodo in hamiltonCycle2]
        print(circ)
        print(len(circ))
    # print(peso1)
    

        peso2 = computeWeight(hamiltonCycle2, g)
        print(peso2)
    
    #print("*"*40) 
    #print("peso atteso (approx_tsp): ", sol_ottime[g.n_nodi], "peso ottenuto: ", peso1)
    #print("approx_tsp fornisce un' approssimazione di", (peso1)/sol_ottime[g.n_nodi])
    
    #print("peso atteso (closest): ", sol_ottime[g.n_nodi], "peso ottenuto: ", peso2)
        print("closest fornisce un' approssimazione di", (peso2)/sol_ottime[g.n_nodi]) 
    #print()
    #print("*"*40)

# for grafo in lista_grafi:
#     if grafo.n_nodi == 16:
#         g = grafo

# for row in g.adj_matrix:
#     print(row)

# hamiltonCycle = approx_tsp_tour(g)
# print("ciclo hamiltonyano:")
# for nodo in hamiltonCycle:
#     print(nodo.id)
# peso = computeWeight(hamiltonCycle, g)
# print ("peso:", peso)
# #questa parte serve per scrivere su un file la matrice di adiacenza di un grafo
        # matrix = g.adj_matrix
        # matrix.pop(0)

        # for row in matrix:
        #     del row[0]


        # with open('matrix.txt', 'w') as filehandle:
        #     filehandle.writelines("%s\n" % str(row)[1:-1] for row in matrix )









