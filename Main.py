from Grafo import Grafo
from Nodo import Nodo
from Arco import Arco
from heap import heap, HeapDecreaseKey, HeapExtractMin, HeapMinimum, BuildMinHeap, isIn
from Utility import merge, mergeSort_weight, inizializzaGrafo, dfs_ciclo, findSet, union, makeSet, test_albero_supporto, test_total_supporto, output_peso, test_tot_pesi
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

#lista di grafi prim
p_g = []
#lista grafi kruskal
k_g = []
#lista grafi kruskal naive
kn_g = []

#lista dei tempi di prim
p_t = [] 
#lista dei tempi di kruskal
k_t = []
#lista dei tempi di kruakl naive
kn_t = []


directory = "mst_dataset/"
lista_grafi = []



def parsing(directory):
    for file in os.listdir(directory):
            crea_grafi(file)



#funzione che dato un path, aggiunge un oggetto grafo 
#alla lista lista_grafi
def crea_grafi(path):

    global lista_grafi
    g = Grafo()
    id2Node = {}
    lista_nodi = set()
    lista_archi = []
    lista_adiacenza = {}
    lista_adiacenza_nodi = {}
    
    f = open("mst_dataset/" + path, "r")

    #assegno i valori numero nodi e numero archi
    prima_riga = f.readline().split(" ")
    g.n_nodi = int(prima_riga[0]) 
    g.n_archi = int(prima_riga[1])
    
    #creo lista di stringhe "nodo1, nodo2, peso"
    righe = f.read().splitlines()
    
    #divido le stringhe in liste di 3 valori [nodo1, nodo2, peso]
    lista_valori = []
    for riga in righe:
        lista_valori.append(riga.split())
    f.close()
        

    #creo il set di nodi e lista archi
    for i in range(0, len(lista_valori)):
        #valori estratti dal file
        nodo_1 = lista_valori[i][0]
        nodo_2 = lista_valori[i][1]
        peso = lista_valori[i][2]
        arco_1 = Arco(nodo_1, nodo_2, peso)
        
        lista_nodi.add(nodo_1)
        lista_nodi.add(nodo_2)
        lista_adiacenza.setdefault(nodo_1, [])    #inzializzo ogni chiave nodo a un valore list
        lista_adiacenza.setdefault(nodo_2, [])    
        lista_adiacenza_nodi.setdefault(nodo_1, [])
        lista_adiacenza_nodi.setdefault(nodo_2, [])

        lista_archi.append(arco_1)
    
    #creo gli oggetti nodo e il dizionario id2Node
    for nodo in lista_nodi:
        obj_nodo = Nodo(nodo)
        id2Node[obj_nodo.nodo] = obj_nodo

    #riempio le liste di adicenza create in precedenza
    for i in range(0, len(lista_valori)):
        nodo_1 = lista_valori[i][0]
        nodo_2 = lista_valori[i][1]
        peso = lista_valori[i][2]
        lista_adiacenza_nodi[nodo_1].append(id2Node[nodo_2])
        lista_adiacenza_nodi[nodo_2].append(id2Node[nodo_1])
        lista_adiacenza[nodo_1].append(Arco(nodo_1, nodo_2, peso))      #arco(u,v)
        lista_adiacenza[nodo_2].append(Arco(nodo_2, nodo_1, peso))      #arco(v,u)
    
    #setto gli attributi dell'arco
    g.id2Node = id2Node
    g.lista_nodi = lista_nodi
    g.lista_archi = lista_archi
    g.lista_adiacenza = lista_adiacenza
    g.lista_adiacenza_nodi = lista_adiacenza_nodi

    
    lista_grafi.append(g)




def measure_run_time(n_instances, graphs, algorithm):
    sum_times = 0

    if graphs[0].n_nodi <=100:         #per avere valori più precisi le istanze con un basso numero di nodi vengono ripetute più volte
        iterations = 30
    else:
        iterations = 1
    #liste per confrontare gli algoritmi
    global p_g
    global k_g
    global kn_g
    global p_t 
    global k_t 
    global kn_t


    print("testing graph size: ", graphs[0].n_nodi)
    for i in range(n_instances):
        print("istanza numbero: ",i)
        if algorithm == "prim":
            gc.disable()
            nodo_casuale = next(iter(graphs[i].lista_nodi))    #casuale perchè il set lista_nodi cambia ordine ad ogni parsing

            start_time = perf_counter_ns()
            m = 0
            while m < iterations:
                prim(graphs[i],graphs[i].getNodo(nodo_casuale))
                m+=1
            end_time = perf_counter_ns()
            p_g.append(prim(graphs[i],graphs[i].getNodo(nodo_casuale)).getGrafoPrim())
            p_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "NaiveKruskal":
            gc.disable()
            start_time = perf_counter_ns()
            j = 0
            while j < iterations:
                naiveKruskal(graphs[i])
                j+=1
            end_time = perf_counter_ns()
            kn_g.append(naiveKruskal(graphs[i]))
            kn_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "Kruskal":
            gc.disable()
            start_time = perf_counter_ns()
            k = 0
            while k < iterations:
                kruskal(graphs[i])     
                k += 1
            end_time = perf_counter_ns()
            k_g.append(kruskal(graphs[i]))
            k_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        sum_times += (end_time - start_time)/iterations


    avg_time = round((sum_times / n_instances)//1000, 3) #millisecondi

    return avg_time



def measurePerformance():
    graphs_groupped = defaultdict(list)
    
    #raggruppo i grafi in base alla dimensione dei loro nodi con un dizionario key:n_nodi, value: grafi con quel numero di nodi        
    for i in range (len(lista_grafi)):
        graphs_groupped[int(lista_grafi[i].n_nodi)].append(lista_grafi[i])

    #  ghhhh il dizionario in base alla key (numero di nodi)
    graphs_groupped = collections.OrderedDict(sorted(graphs_groupped.items()))
    

    #per calcolare la costante considero ElgV quindi per ogni dimensione di grafo prendo il numero di nodi e la media del numero degli archi
    sizes = []
    arches = 0
    for key in graphs_groupped.keys():
        for g in graphs_groupped[key]:
            arches += g.n_archi
            nodes = g.n_nodi
        avg_arches = arches / len(graphs_groupped[key])
        sizes.append([nodes, avg_arches])
        arches = 0
        nodes = 0

    algorithmsToTest = ["prim", "Kruskal", "NaiveKruskal"]
    totTimes = []
    totRatios = []
    totConstant = []
    for algorithm in algorithmsToTest:
        print("sto testando", algorithm)
        times = [measure_run_time(len(graphs_groupped[key]), graphs_groupped[key], algorithm) for key in graphs_groupped]
        totTimes.append(times)
        ratios = [None] + [round(times[i+1]/times[i],3) for i in range(len(sizes)-1)] 
        totRatios.append(ratios)

        if algorithm == "NaiveKruskal":
            totConstant.append([round(times[i]/(sizes[i][1] *sizes[i][0]),3) for i in range(len(sizes))])

        else:
            totConstant.append([round(times[i]/(sizes[i][1] * math.log(sizes[i][0])),3) for i in range(len(sizes))])

    return totTimes, totRatios, totConstant, sizes, graphs_groupped
    


def plot_graph():
    
    #misuro le performance per ogni algoritmo, i valori times, ratios, constant sono matrici di dimensione 4*n n sono il numero di dimensioni dei grafi
    [times, ratios, constant, sizes, graphs_groupped] = measurePerformance()
    algorithmsToTest = ["prim","Kruskal", "NaiveKruskal"]

    for i in range(len(algorithmsToTest)):
        print ("Algoritmo:", algorithmsToTest[i])
        print("Size\t\ttTime(ms)\t\tCostant\t\tRatio")

        print(65*"-")
        for j in range(len(sizes)):
            if j < 10:
                print(sizes[j][0], '' , times[i][j], '', '', constant[i][j], '', ratios[i][j] ,sep="\t")
            else:
                print(sizes[j][0], '', times[i][j], '', constant[i][j], '', ratios[i][j], sep="\t")
        print(65*"-")


    #grafico dei tempi
        reference = []
        print("costante utilizzata per calcolare la reference :", algorithmsToTest[i], " ",constant[i][len(constant[0]) - 1] )
        if algorithmsToTest[i] == "NaiveKruskal":
            for j in range (len(sizes)):
                reference.append (constant[i][len(constant[0]) - 1] * sizes[j][1] * sizes[j][0])
        else:
            for j in range (len(sizes)):
                reference.append (constant[i][len(constant[0]) - 1] * sizes[j][1] * math.log(sizes[j][0]))

        plt.plot(graphs_groupped.keys(), times[i], graphs_groupped.keys(), reference)
        plt.title("performance " + algorithmsToTest[i])
        plt.ylabel('run time(ns)')
        plt.xlabel('size')
        plt.show()

    plt.plot(graphs_groupped.keys(), times[0], label = 'Prim')
    plt.plot(graphs_groupped.keys(), times[1],label = 'Kruskal')
    plt.plot(graphs_groupped.keys(), times[2], label = 'Kruskal naive')
    plt.legend()
    plt.title("grafici in relazione")
    plt.ylabel('run time(ns)')
    plt.xlabel('size')
    plt.show()

    plt.plot(graphs_groupped.keys(), times[0], label = 'Prim')
    plt.plot(graphs_groupped.keys(), times[1],label = 'Kruskal')
    plt.legend()
    plt.title("grafici in relazione")
    plt.ylabel('run time(ns)')
    plt.xlabel('size')
    plt.show()

    return graphs_groupped, times

 

def prim(g, radice):
    g.totPeso = 0
    radice.padre = radice.nodo
    lista_nodi_obj = g.getListaNodi()
    index = 0
    for nodo in lista_nodi_obj:
        nodo.in_h = 1
        nodo.key = float('inf')  #float('inf') indica un valore superiore a qualsiasi altro valore
        nodo.heapIndex = index  #per non usare la funzione 'index' 
        index = index + 1
    radice.key = 0
    q = heap(lista_nodi_obj)
    BuildMinHeap(q)
    while q.heapsize != 0:
        u = HeapExtractMin(q)
        if u.key == float('inf'):
            exit()
        g.totPeso += u.key
        for arco in g.lista_adiacenza[u.nodo]:      #per ogni arco, in lista di adiacenza di u
            nodo_adj = g.getNodo(arco.nodo2)        #g.getNodo(arco.nodo2) = (oggetto) nodo adiacente a u
            if isIn(nodo_adj) == 1 and arco.peso < nodo_adj.key:
                nodo_adj.padre = u.nodo
                index = nodo_adj.heapIndex  #ottengo la sua posizione all'interno dell'heap
                HeapDecreaseKey(q, index, arco.peso)
    return g


# NOTA IMPORTANTE
# durante la costruzione del mst si potrebbero formare sottografi non connessi tra loro
# tuttavia non è necessario eseguire la dfs_ciclo per ognuno dei sottografi non connessi
# infatti, se al passo n il grafo non presenta cicli, al passo n+1, facendo iniziare la visita dfs
# dal nodo (o da uno dei nodi) dell'arco aggiunto, questa compirà una visita completa del sottografo connesso
# il quale è appunto l'unico che al passo n+1 potrebbe contenere un ciclo.
def naiveKruskal(g):
    g.totPeso = 0
    grafo_mst = Grafo()
    prova_mst = Grafo()

    mergeSort_weight(g.lista_archi, 0, len(g.lista_archi)-1)
    
    inizializzaGrafo(prova_mst, g)
    inizializzaGrafo(grafo_mst, g)

    for arco in g.lista_archi:
        if grafo_mst.n_archi != g.n_nodi - 1:
            prova_mst.lista_adiacenza_nodi[arco.nodo1].append(prova_mst.getNodo(arco.nodo2))
            prova_mst.lista_adiacenza_nodi[arco.nodo2].append(prova_mst.getNodo(arco.nodo1))
            padri = [0]*(g.n_nodi+1)
            visitati = [0]*(g.n_nodi+1)

            if not dfs_ciclo(prova_mst, g.getNodo(arco.nodo2), padri, visitati):
                grafo_mst.totPeso += arco.peso
                grafo_mst.aggiungiArco(arco)

            else:
                prova_mst.lista_adiacenza_nodi[arco.nodo1].pop()
                prova_mst.lista_adiacenza_nodi[arco.nodo2].pop()
        else:
            return grafo_mst

    return grafo_mst




def kruskal(g):
    g.totPeso = 0
    grafo = Grafo()

    inizializzaGrafo(grafo, g)
    
    for v in grafo.getListaNodi():
        makeSet(v)

    mergeSort_weight(g.lista_archi, 0, len(g.lista_archi)-1)
    
    for arco in g.lista_archi:
        if grafo.n_archi != g.n_nodi - 1:
            if findSet(grafo, grafo.getNodo(arco.nodo1)) != findSet(grafo, grafo.getNodo(arco.nodo2)):
                grafo.totPeso += arco.peso
                grafo.aggiungiArco(arco)
                union(grafo.getNodo(arco.nodo1), grafo.getNodo(arco.nodo2), grafo)
        else:
            return grafo
    
    return grafo



######################## MAIN ########################

parsing(directory)

lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.n_nodi, grafo.n_archi))

graphs_groupped,times = plot_graph()

test_total_supporto(p_g, kn_g, k_g)

output_peso(p_g, k_g, kn_g, lista_grafi, p_t, k_t, kn_t)

test_tot_pesi(p_g, k_g, kn_g)



