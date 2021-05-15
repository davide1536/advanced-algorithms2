from Grafo import Grafo
from Nodo import Nodo
from Arco import Arco
from Utility import convert, calcEuclDist, calcGeoDist, prim, preOrderVisit, getTree, output_peso
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
import random
import time
import sys


#per_m = "algoritmi-avanzati-laboratorio2/"
per_m = ""
directory = per_m+"tsp_dataset/"
lista_grafi = []
sol_parziale = {}

#liste contentenenti i pesi risultanti dagli algoritmi
peso_held_karp = []
peso_euristica = []
peso_due_approssimato = []

##liste contentenenti i tempi di esecuzione degli algoritmi
#tempi fittizi per test
tempo_held_karp = [0.1]*13
tempo_euristica = [0.1]*13
tempo_due_approssimato = [0.1]*13


#funzione che controlla l'unicità di ogni nodo all'interno dei ciruito
def checkUniq(c):
    for nodo in c:
        occorrenze = c.count(nodo)
        if occorrenze > 1 and nodo != 1:
            return False
    return True


#funzione che controlla se il ciclo restituito è un ciclo hamiltoniano
def checkHamiltoCycle(g, c):
    if (len(c) == g.n_nodi + 1) and (checkUniq(c) == True):
        return True
    else:
        return False

#funzione che calcola i pesi, dato un circuito c e un grafo g
def computeWeight(c, g):
    pesoCiclo = 0
    for i,nodo in enumerate(c):
        if i != (len(c)-1): 
            nextNode = c[i+1]
            pesoCiclo += g.adj_matrix[nodo][nextNode]
            # print("nodo ", nodo, "vicino ", c[i+1])
            # print("peso ", g.adj_matrix[nodo][nextNode])

    return pesoCiclo


def parsing(directory):
    for file in os.listdir(directory):
            crea_grafi(file)


#funzione che dato un path, aggiunge un oggetto grafo 
#alla lista lista_grafiw
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
    #radice = random.choice(g.lista_nodi)
    radice = g.getNodo(1)

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
    #conversione ciclo hamiltoniano da oggetti a interi
    for i,nodo in enumerate(hamiltonCycle):
        hamiltonCycle[i] = nodo.id

    return hamiltonCycle


############################################### HELD-KARP ###############################################

#algoritmo esatto Held e Karp
def hkVisit(g,v,S, start):
    global sol_parziale
    PERIOD_OF_TIME = 5 #180
    new_set_node = []

    #creo un id univoco per ogni coppia v,S
    id_vS = [v]
    id_vS.append(S)
    id_vS = str(id_vS)

    #caso base
    if S == [v]:
        return g.adj_matrix[1][v]
    
    #coppia già calcolata
    elif id_vS in g.diz_pesi:
        return g.diz_pesi[id_vS] 
    
    else:
        #inizio creazione sottoinsieme
        g.diz_pesi[id_vS] = None
        g.diz_padri[id_vS] = None
        #fine creazione sottoinsieme
        
        mindist = math.inf
        minprec = None
        new_set_node[:] = S
        new_set_node.remove(v)
        for u in new_set_node:
            dist = hkVisit(g, u, new_set_node, start)
            if dist + g.adj_matrix[u][v] < mindist:
                mindist = dist + g.adj_matrix[u][v]
                minprec = u
        g.diz_pesi[id_vS] = mindist
        g.diz_padri[id_vS] = minprec
        
        #costruisco la soluzione parziale
        if g not in sol_parziale:
            sol_parziale[g] = [id_vS, S, mindist]
        else:
            if len(sol_parziale[g][1]) < len(S):
                sol_parziale[g] = [id_vS, S, mindist]
        
        if time.time() > start + PERIOD_OF_TIME : 
            #print("timeout raggiunuto!")
            #print("peso parziale:", sol_parziale[g][2])
            #print("nodi circuito parziale:", sol_parziale[g][0])
            peso_held_karp.append(sol_parziale[g][2])
            raise HaltException()

        
        return mindist



#funzione per chiamare l'algorirmo Held e Karp
def hkTsp(g): 
    start = time.time()
    return hkVisit(g, 1, g.lista_id_nodi, start)



############################################### CLOSEST_INSERTION ###############################################


def updateCiclo(nodo, ciclo, verticiCiclo, noCiclo, position):
    noCiclo.remove(nodo)
    verticiCiclo.append(nodo)
    ciclo.insert(position, nodo)


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

    for index,nodo in enumerate(ciclo):
        if index!= (len(ciclo)-1):
            i = ciclo[index]
            j = ciclo[index+1]
            peso_i_k = g.adj_matrix[i][k]
            peso_k_j = g.adj_matrix[k][j]
            peso_i_j = g.adj_matrix[i][j]
            peso = peso_i_k + peso_k_j - peso_i_j
            if peso < minPeso:
                minPeso = peso
                min_i = i
                min_j = j

               
    return min_i, min_j

  
def closest_insertion(g):
    #tengo traccia dei nodi nel circuito parziale attraverso queste 2 liste
    verticiNonCiclo = copy.deepcopy(g.lista_id_nodi) 
    verticiCiclo = []
    circuitoParziale = [] #lista contenente il circuito parziale
    #radice = random.choice(g.lista_nodi)

    radice = 1 #indico con nodo_k il nodo da inserire all'interno del circuito parziale
    updateCiclo(radice, circuitoParziale, verticiCiclo, verticiNonCiclo,0)
    #Il primo passo dell'algoritmo viene fatto "a mano" al di fuori del ciclo
    nodo_k = getClosestNode(g, verticiCiclo, verticiNonCiclo)
    #node_i = getPosition(g, nodo_k, circuitoParziale, verticiNonCiclo)
    #g.totPeso += min_peso
    position = circuitoParziale.index(1)
    updateCiclo(nodo_k, circuitoParziale,verticiCiclo, verticiNonCiclo, position+1)
    circuitoParziale.append(radice)

    while len(verticiNonCiclo) != 0: #finche non ho inserito tutti i vertici
        #if len(circuitoParziale) == 2:
        #    circuitoParziale.append(1)
        nodo_k = getClosestNode(g, verticiCiclo, verticiNonCiclo)
        node_i, node_j = getPosition(g, nodo_k, circuitoParziale, verticiNonCiclo)
        #print("nodo i:", node_i, "nodo j: ",node_j)
        #g.totPeso += min_peso
        #print("circuito")
        #print([nodo for nodo in circuitoParziale])
        #print("nodo precedente", node_i, "nodo da aggiungere", nodo_k)
        position_i = circuitoParziale.index(node_i)
        position_j = circuitoParziale.index(node_j)

        #print("position i:", position_i, "position j", position_j)
        updateCiclo(nodo_k, circuitoParziale,verticiCiclo, verticiNonCiclo, position_i+1)

    #circuitoParziale.append(1)     
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
    




################################################ SOLUZIONI PARZIALI ################################################

class HaltException(Exception):
    pass


#funzione per l'esecuzione di hkTsp entro 3 minuti
def main_hkTsp(g):
    
    #for g in lista_grafi:
    #print()
    #print("-"*40)
    #print("eseguo grafo con:", g.n_nodi, "nodi")
    try:
        peso = hkTsp(g)
        peso_held_karp.append(peso)
        #print("peso:", peso)
    except HaltException as error:
        pass
    except RecursionError as re:
        #print("Errore:")
        #print("maximum recursion depth exceeded")
        if g in sol_parziale:
            #print("peso parziale:", sol_parziale[g][2])
            #print("circuito parziale:", sol_parziale[g][0])
            peso_held_karp.append(sol_parziale[g][2])
        else: 
            #print("non ci sono soluzioni per questo grafo")
            peso_held_karp.append(1)

    #print("-"*40)


def main():
    for g in lista_grafi:
        main_hkTsp(g)
        
        hamiltonCycle1 = approx_tsp_tour(g)
        peso_due_approssimato.append(computeWeight(hamiltonCycle1, g))
        
        hamiltonCycle2 = closest_insertion(g)
        peso_euristica.append(computeWeight(hamiltonCycle2, g))

    output_peso(lista_grafi, peso_held_karp, peso_euristica, peso_due_approssimato, tempo_held_karp, tempo_euristica, tempo_due_approssimato)
    

        



################################################ MAIN ################################################

parsing(directory)

print("fine parsing")

lista_grafi = sorted(lista_grafi, key=lambda grafo: grafo.n_nodi)

main()







# matrice = [[0,0,0,0,0], [0,0,    4,    1,    3], [0,   4 ,   0,    2,    1], [0,   1,    2,    0,    5], [0  , 3,    1,    5,    0]]
# grafo_prova = Grafo()
# n_nodi = 4
# lista_id_nodi = [1,2,3,4]

# grafo_prova.n_nodi = n_nodi
# grafo_prova.adj_matrix = matrice
# grafo_prova.lista_id_nodi = lista_id_nodi

# lista_grafi.append(grafo_prova)


#for g in lista_grafi:
    #if g.n_nodi == 16:
#         for i in g.lista_id_nodi:
#           print(i, g.getNodo(i).x, g.getNodo(i).y)
        #for j in g.adj_matrix:
        #    print(j)
        #print("***********************************")
        #peso = hkTsp(g)
        #p = g.diz_pesi['[1, [1, 2, 3, 4]]']
        #print("peso:", peso)
        #print("sol_parziale", sol_parziale[g][0], sol_parziale[g][2])
        #print(len(g.diz_pesi.keys()))
        #for vs in g.diz_pesi.keys():
        #    print(vs)

        #print("***********************************")
#         for nodo in g.id2NodeSet.keys():
#             print("id:",nodo, "nodo:", g.id2NodeSet[nodo].v, "subset:", g.id2NodeSet[nodo].S)
#         print(len(g.id2NodeSet.keys()))

#         peso = hkTsp(g)
#         print(peso)
        
#         for i in g.diz_padri.keys():
#             print((i.v, i.S), g.diz_pesi[i])

#         for i in g.id2NodeSet.keys():
#            print(i, g.id2NodeSet[i])

# sol_ottime = { 8 : 14,
#                14 : 3323, 
#                16 : 6859, 
#                22 : 7013,
#                51 : 426,
#                52 : 7542,
#                100 : 21294,
#                #100 : 21282,
#                150 : 6528,
#                202 : 40160,
#                229 : 134602,
#                442 : 50778,
#                493 : 35002,
#                1000 : 18659688 }


""" for g in lista_grafi:
    if g.n_nodi != 4:
        print("grafo con: ", g.n_nodi, "nodi")

        hamiltonCycle1 = approx_tsp_tour(g)

        #hamiltonCycle2 = closest_insertion(g)
        hamiltonCycle2 = closest_insertion(g)

        #controllo se sono effettivamente cicli hamiltoniani quelli restituiti
        if (checkHamiltoCycle(g, hamiltonCycle1) == False) or (checkHamiltoCycle(g, hamiltonCycle2) == False):
            print("ha dato problemi il grafo con ", g.n_nodi, "nodi")
            exit(0)

        #converto in oggetti i clicli ottenuti
        #circ = [nodo.id for nodo in hamiltonCycle2]
        #circ = [g.getNodo(nodo) for nodo in hamiltonCycle2]
        # print(circ)
        # print(len(circ))
        #print(peso1)

        peso1 = computeWeight(hamiltonCycle1, g)        #print(peso2)
        peso2 = computeWeight(hamiltonCycle2, g)

        print("*"*40) 
        print("peso atteso (approx_tsp): ", sol_ottime[g.n_nodi], "peso ottenuto: ", peso1)
        print("approx_tsp fornisce un' approssimazione di", (peso1)/sol_ottime[g.n_nodi])

        print("peso atteso (closest): ", sol_ottime[g.n_nodi], "peso ottenuto: ", peso2)
        print("closest fornisce un' approssimazione di", (peso2)/sol_ottime[g.n_nodi]) 

        print()
        print("*"*40) """
    

# for grafo in lista_grafi:
#     if grafo.n_nodi == 8:
#         g = grafo

# #hamiltonCycle = closest_insertion(g)
# hamiltonCycle = approx_tsp_tour(g)
# print("ciclo hamiltonyano:")
# print(hamiltonCycle)
# print(checkHamiltoCycle(g, hamiltonCycle))
# peso = computeWeight(hamiltonCycle, g)


# print("peso atteso (closest): ", sol_ottime[g.n_nodi], "peso ottenuto: ", peso)
# print("closest fornisce un' approssimazione di", (peso)/sol_ottime[g.n_nodi]) 
# #print("closest fornisce un' approssimazione di", (peso2)/sol_ottime[g.n_nodi]) 
# #questa parte serve per scrivere su un file la matrice di adiacenza di un grafo
# matrix = g.adj_matrix
# matrix.pop(0)

# for row in matrix:
#     del row[0]


# with open('matrix.txt', 'w') as filehandle:
#     filehandle.writelines("%s\n" % str(row)[1:-1] for row in matrix )










