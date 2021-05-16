from Nodo import Nodo
from Grafo import Grafo
from NodeSet import NodeSet
import math
from heap import heap, HeapDecreaseKey, HeapExtractMin, BuildMinHeap, isIn
from tabulate import tabulate
from Grafo import Grafo
from Nodo import Nodo
from Arco import Arco
from Utility import *
from NodeSet import NodeSet
import random
import os
per_m = ""
directory = per_m+"tsp_dataset/"
lista_grafi = []
sol_parziale = {}

#funzione per convertire le coordinate in radianti
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
def convert(x):
    PI = 3.141592
    #deg = round(x)
    deg = int(x)
    min = x - deg
    rad = PI * (deg + 5.0 * min/3.0) / 180.0
    #rad = round(PI * (deg + 5.0 * min/3.0) // 180.0)
    return rad



def calcGeoDist(nodo1, nodo2):
    RRR = 6378.388
    q1 = math.cos(nodo1.y - nodo2.y)
    q2 = math.cos(nodo1.x - nodo2.x)
    q3 = math.cos(nodo1.x + nodo2.x)
    dist = int(RRR * math.acos(0.5*((1.0 + q1)*q2 - (1.0 - q1)*q3)) + 1.0)
    return dist



def calcEuclDist(nodo1, nodo2):
    dist = round(math.sqrt((nodo1.x - nodo2.x)**2 + (nodo1.y - nodo2.y)**2))
    return dist



#funzione per inizializzare le coppie v,S
def creaSottoinsiemi(grafo):
    x = [i for i in range(2,grafo.n_nodi+1)]
    s = [0]*(grafo.n_nodi)
    sub_seq(grafo, grafo.n_nodi-1, 0, [], x, s)



#crea sequenze
def sub_seq(grafo, n,i,g,x, s):
    if(i==n):
        diz_k = []
        for el in range(0,n):
            if(s[el]!=0):
                g.sort()
                g.append(x[el])
                diz_k.append(x[el])
        for key in diz_k:
            nodeSet = NodeSet()
            nodeSet.v = key
            nodeSet.S = g
            v = [key]       #creo un id univoco per ogni coppia v,S da inserire nel dizionario id2NodeSet
            v.append(g)
            grafo.id2NodeSet[str(v)] = nodeSet
            if len(g) == 1:
                grafo.diz_pesi[nodeSet] = grafo.adj_matrix[i][1]
                grafo.diz_padri[nodeSet] = 1
            else:
                grafo.diz_pesi[nodeSet] = None
                grafo.diz_padri[nodeSet] = None
        return
    for num in [0,1]:
      s[i]=num
      sub_seq(grafo, n, i+1, [], x, s)




def prim(g, radice):
    g.totPeso = 0
    #radice.padre = radice.id
    lista_nodi_obj = g.getListaNodi()
    index = 0
    for nodo in lista_nodi_obj:
        nodo.padre = None
        nodo.figlio = []
        nodo.in_h = 1
        nodo.key = float('inf')  #float('inf') indica un valore superiore a qualsiasi altro valore
        nodo.heapIndex = index  #per non usare la funzione 'index' 
        index = index + 1
    radice.key = 0
    q = heap(lista_nodi_obj)
    BuildMinHeap(q)
    while q.heapsize != 0:
        u = HeapExtractMin(q)
        g.totPeso += u.key
        for i,peso_adj in enumerate(g.adj_matrix[u.id][1:], 1):      #recupero i pesi dei nodi adiacenti ad u 
            #if i != u.id: #qui considero  tutti i vicini del nodo u tranne u stesso
                if isIn(g.getNodo(i)) == 1 and peso_adj < g.getNodo(i).key:
                    g.getNodo(i).padre = u
                    index = g.getNodo(i).heapIndex  #ottengo la sua posizione all'interno dell'heap
                    HeapDecreaseKey(q, index, peso_adj)
    return g



def getTree(g):
    for nodo in g.lista_nodi:
        if nodo.padre != None:
            nodo.padre.figlio.append(nodo)



def preOrderVisit(nodo, h):
    h.append(nodo)
    #print("pre order visit ", nodo.id)
    for figlio in nodo.figlio:
        preOrderVisit(figlio, h)
    return h
         

#funzione min per confronti a 3 
# list = [peso_held_karp, peso_euristica, peso_due_approssimato]
def min_reloaded(list, i):
    algo = ""
    min_peso = 0
    if i < 2:
        if list[0] < list[1]:
            min_peso = list[0]
            algo = "peso_held_karp"
        elif list[0] > list[1]:
            min_peso = list[1]
            algo = "peso_euristica"
        else:
            min_peso = list[0]
            algo = "prim == kruskal"

        if min_peso > list[2]:
            min_peso = list[2]
            algo = "peso_due_approssimato"
    else:
        min_peso = min(list[1], list[2])
        if min_peso == list[1]:
            algo = "peso_euristica"
        else:
            algo = "peso_due_approssimato"
    
    res = algo + " : " + str(min_peso)
    return res



#funzione per la creazione di tabelle dei risultati
def output_peso(lista_grafi, peso_held_karp, peso_euristica, peso_due_approssimato, tempo_held_karp, tempo_euristica, tempo_due_approssimato):

    errore_held_karp = []
    errore_euristica = []
    errore_due_approssimato = []

    sol_ottime = [3323, 6859, 7013, 426, 7542, 21294, 21282, 6528, 40160, 134602, 50778, 35002, 18659688]
    
    #calcolo l'errore
    for i in range(len(lista_grafi)):
        #(soluzione_trovata - soluzione_ottima)/soluzione_ottima
        errore_held_karp.append(round((peso_held_karp[i] - sol_ottime[i])/sol_ottime[i],3))
        errore_euristica.append(round((peso_euristica[i] - sol_ottime[i])/sol_ottime[i],3))
        errore_due_approssimato.append(round((peso_due_approssimato[i] - sol_ottime[i])/sol_ottime[i],3))

    #creo tabella da cui prendere i dati
    table = []
    table.append([grafo.name for grafo in lista_grafi])                 #table[0]
    
    table.append([peso for peso in peso_held_karp])                     #table[1]
    table.append([tempo for tempo in tempo_held_karp])                  #table[1]
    table.append([errore for errore in errore_held_karp])               #table[3]
    
    table.append([peso for peso in peso_euristica])                     #table[4]
    table.append([tempo for tempo in tempo_euristica])                  #table[5]
    table.append([errore for errore in errore_euristica])               #table[6]
    
    table.append([peso for peso in peso_due_approssimato])              #table[7]
    table.append([tempo for tempo in tempo_due_approssimato])           #table[8]
    table.append([errore for errore in errore_due_approssimato])        #table[9]

    #tabella con i valori inseriti
    tabella = []
    for i in range(len(lista_grafi)):
        tabella.append([table[0][i], table[1][i], table[2][i], table[3][i], table[4][i], table[5][i], table[6][i], table[7][i], table[8][i], table[9][i], min_reloaded([table[1][i], table[4][i], table[7][i]], i)])

    print()
    print(tabulate(tabella, headers= ["istanza", "peso_held_karp", "tempo_held_karp", "errore_held_karp", "peso_euristica", "tempo_euristica", "errore_euristica", "peso_due_approssimato", "tempo_due_approssimato", "errore_due_approssimato", "algoritmo migliore"], tablefmt='pretty'))








