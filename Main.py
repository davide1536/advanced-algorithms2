from Utility import *
import math
import gc
from time import perf_counter_ns
import copy
import time

#per_m = "algoritmi-avanzati-laboratorio2/"
# per_m = ""
# directory = per_m+"tsp_dataset/"
#lista_grafi = []
#sol_parziale = {}
times = []

#liste contentenenti i pesi risultanti dagli algoritmi
peso_held_karp = []
peso_euristica = []
peso_due_approssimato = []



def measureRunTime(algorithm):
    times = []
    for g in lista_grafi:
        
        if algorithm == "held karp":
            gc.disable()
            start_time = perf_counter_ns()
            #inizio calcolo tempi
            main_hkTsp(g)
            #fine calcolo tempi
            end_time = perf_counter_ns()
            gc.enable()

        elif algorithm == "closest insertion":
            gc.disable()
            start_time = perf_counter_ns()
            #inizio calcolo tempi
            hamiltonCycle2 = closest_insertion(g)
            #fine calcolo tempi
            end_time = perf_counter_ns()
            #aggiorno lista pesi
            peso_euristica.append(computeWeight(hamiltonCycle2, g))
            gc.enable()

        elif algorithm == "approx tsp tour":
            gc.disable()
            start_time = perf_counter_ns()
            #inizio calcolo tempi
            hamiltonCycle1 = approx_tsp_tour(g)
            #fine calcolo tempi
            end_time = perf_counter_ns()
            #aggiorno lista pesi
            peso_due_approssimato.append(computeWeight(hamiltonCycle1, g))
            gc.enable()

        avg_time = round((end_time - start_time)//1000, 3)

        times.append(avg_time)

    return times


def measurePerformance():
    algorithmsToTest = ["held karp", "closest insertion", "approx tsp tour"]
    totalTimes = []
    times = []
    for algorithm in algorithmsToTest:
        times = measureRunTime(algorithm)
        totalTimes.append(times)
    return totalTimes



############################################### 2-APPROSSIMATO ###############################################



#algoritmo 2-approssimato
def  approx_tsp_tour(g):
    h = []
    radice = g.getNodo(1)
    prim(g, radice)

    getTree(g)
    h = preOrderVisit(radice, h)
    h.append(radice)
    hamiltonCycle = h
    #conversione ciclo hamiltoniano da oggetti a interi
    for i,nodo in enumerate(hamiltonCycle):
        hamiltonCycle[i] = nodo.id

    return hamiltonCycle


############################################### HELD-KARP ###############################################

#algoritmo esatto Held e Karp
#prende in input il grado, una coppia (vertice v, sottoinsieme S) e il tempo di inizio dell'esecuzione
def hkVisit(g,v,S, start):
    global sol_parziale
    PERIOD_OF_TIME = 3
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
        #inizializzo diz_pesi e diz_padri con il nuovo sottoinsieme
        g.diz_pesi[id_vS] = None
        g.diz_padri[id_vS] = None
        
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
        
        #calcolo dei 3 minuti
        if time.time() > start + PERIOD_OF_TIME : 
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

    radice = 1 #indico con nodo_k il nodo da inserire all'interno del circuito parziale
    updateCiclo(radice, circuitoParziale, verticiCiclo, verticiNonCiclo,0)
    #Il primo passo dell'algoritmo viene fatto "a mano" al di fuori del ciclo
    nodo_k = getClosestNode(g, verticiCiclo, verticiNonCiclo)
   
    position = circuitoParziale.index(1)
    updateCiclo(nodo_k, circuitoParziale,verticiCiclo, verticiNonCiclo, position+1)
    circuitoParziale.append(radice)

    while len(verticiNonCiclo) != 0: #finche non ho inserito tutti i vertici
      
        nodo_k = getClosestNode(g, verticiCiclo, verticiNonCiclo)
        node_i, node_j = getPosition(g, nodo_k, circuitoParziale, verticiNonCiclo)
        position_i = circuitoParziale.index(node_i)
        # position_j = circuitoParziale.index(node_j)

        updateCiclo(nodo_k, circuitoParziale,verticiCiclo, verticiNonCiclo, position_i+1)

    return circuitoParziale
    



################################################ SOLUZIONI PARZIALI ################################################

class HaltException(Exception):
    pass


#funzione per l'esecuzione di hkTsp entro 3 minuti
def main_hkTsp(g):
    
    try:
        peso = hkTsp(g)
        peso_held_karp.append(peso)
    
    except HaltException as error:
        pass
    
    except RecursionError as re:
        
        if g in sol_parziale:
            peso_held_karp.append(sol_parziale[g][2])
        else:
            peso_held_karp.append(0)

    #print("-"*40)



    



################################################ MAIN ################################################

parsing(directory)

print("fine parsing")

lista_grafi = sorted(lista_grafi, key=lambda grafo: grafo.n_nodi)

times = measurePerformance()

output_peso(lista_grafi, sol_parziale, peso_held_karp, peso_euristica, peso_due_approssimato, times[0], times[1], times[2])
