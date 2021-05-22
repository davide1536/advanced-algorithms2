from Nodo import Nodo
from Grafo import Grafo
import math
from heap import heap, HeapDecreaseKey, HeapExtractMin, BuildMinHeap, isIn
from tabulate import tabulate
from Grafo import Grafo
from Nodo import Nodo
from Utility import *
import matplotlib.pyplot as plt
import os


per_m = ""
directory = per_m+"tsp_dataset/"
lista_grafi = []
sol_parziale = {}

#funzione per convertire le coordinate in radianti
#funzione che controlla l'unicità di ogni nodo all'interno dei ciruito
def plotGraph(closestPesi, approxPesi):
    costante = []
    for i in range(len(closestPesi)):
        costante.append(2)
    plt.plot(range(len(closestPesi)), costante, label="costante 2")
    plt.plot(range(len(closestPesi)), closestPesi, label = 'Pesi closest insertion')
    plt.plot(range(len(closestPesi)), approxPesi, label = 'Pesi approx tsp tour')
    plt.legend()
    plt.ylabel("peso")
    plt.xlabel("grafo")
    plt.show()


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
    g.lista_id_nodi = [n for n in range(1, n_nodi+1)]     
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
    

def minMaxScaling(pesiHk, pesiClosest, pesiApprox, tempiHk, tempiClosest, tempiApprox):
    #normalizzazione pesi
    pesi = pesiHk + pesiClosest + pesiApprox
    #print("i pesi sono", pesi)
    minPeso = min(pesi)
    maxPeso = max(pesi)
    
    pesoHkNorm = []
    pesoClosestNorm = []
    pesoApproxNorm = []

    tempoHkNorm = []
    tempoClosestNorm = []
    tempoApproxNorm = []
    
    for pesoHk in pesiHk:
        pesoHkNorm.append((pesoHk - minPeso) / (maxPeso - minPeso))

    for pesoClosest in pesiClosest:
        pesoClosestNorm.append((pesoClosest - minPeso) / (maxPeso - minPeso))

    for pesoApprox in pesiApprox:
        pesoApproxNorm.append((pesoApprox - minPeso) / (maxPeso - minPeso))
        
    #normalizzazione tempi

    tempi = tempiHk + tempiClosest + tempiApprox
    minTempo = min(tempi)
    maxTempo = max(tempi)
    
    for tempoHk in tempiHk:
        tempoHkNorm.append((tempoHk - minTempo) / (maxTempo - minTempo))

    for tempoClosest in tempiClosest:
        tempoClosestNorm.append((tempoClosest - minTempo) / (maxTempo - minTempo))

    for tempoApprox in tempiApprox:
        tempoApproxNorm.append((tempoApprox - minTempo) / (maxTempo - minTempo))
    
    return pesoHkNorm,pesoClosestNorm,pesoApproxNorm,tempoHkNorm,tempoClosestNorm,tempoApproxNorm



    
    

#funzione min per confronti a 3 
#list = [peso_held_karp, peso_euristica, peso_due_approssimato]
def min_reloaded(list, i):
    pesoHk = list[0]
    tempoHk = list[1]
    pesoClosest = list[2]
    tempoClosest = list[3]
    pesoApprox = list[4]
    tempoApprox = list[5]
    scoreHk = pesoHk * tempoHk
    scoreClosest = pesoClosest * tempoClosest
    scoreApprox = pesoApprox * tempoApprox
    algo = ""
    min_peso = 0
    if i < 2:
        if scoreHk < scoreClosest:
            min_score = scoreHk
            algo = "peso_held_karp"
        elif scoreHk > scoreClosest:
            min_score = scoreClosest
            algo = "peso_euristica"
        else:
            min_score = scoreHk
            algo = "peso_held_karp"

        if min_peso > scoreApprox:
            min_score = scoreApprox
            algo = "peso_due_approssimato"
    else:
        min_score = min(scoreClosest, scoreApprox)
        if min_score == scoreClosest:
            algo = "peso_euristica"
        else:
            algo = "peso_due_approssimato"
    
    res = algo 
    return res



#funzione per il calcolo dell'errore per la soluzione parziale dell'algoritmo held e karp
def calcolo_errore_avanzato(g, i, sol_esatta, sol_parziale, peso_held_karp):
    #trovo il numero di nodi calcolati entro i 3 minuti
    if g in sol_parziale:
        n_nodi_circuito = len(sol_parziale[g][1])
    else: 
        return -1
    
    #errore = (soluzione_trovata - soluzione_ottima) / soluzione_ottima
    #errore_parziale = (soluzione_parziale - soluzione_parziale_ottima) / soluzione_parziale_ottima
    #soluzione_parziale_ottima = x
    # n_nodi_totali : n_nodi_circuito = soluzione_ottima : x
    # x = 
    soluzione_parziale_ottima = (n_nodi_circuito * sol_esatta[i]) / g.n_nodi
    errore_parziale = round((peso_held_karp[i] - soluzione_parziale_ottima) / soluzione_parziale_ottima, 3)
    
    return errore_parziale
    





#funzione per la creazione di tabelle dei risultati
def output_peso(lista_grafi, sol_parziale, peso_held_karp, peso_euristica, peso_due_approssimato, tempo_held_karp, tempo_euristica, tempo_due_approssimato):

    errore_held_karp = []
    errore_euristica = []
    errore_due_approssimato = []
    errore_held_karp_avanzato = []
    rapporto_euristica = []
    rapporto_due_approssimato = []
    #print("PESI:", peso_held_karp, peso_euristica, peso_due_approssimato, tempo_held_karp, tempo_euristica, tempo_due_approssimato)
    sol_ottime = [3323, 6859, 7013, 426, 7542, 21294, 21282, 6528, 40160, 134602, 50778, 35002, 18659688]
    
    pesoHkNorm,pesoClosestNorm,pesoApproxNorm,tempoHkNorm,tempoClosestNorm,tempoApproxNorm = minMaxScaling(peso_held_karp, peso_euristica, peso_due_approssimato, tempo_held_karp, tempo_euristica, tempo_due_approssimato)
    #print("normalizzazione: ", pesoHkNorm,pesoClosestNorm,pesoApproxNorm,tempoHkNorm,tempoClosestNorm,tempoApproxNorm)
    #calcolo l'errore
    for i in range(len(lista_grafi)):
        #(soluzione_trovata - soluzione_ottima)/soluzione_ottima
        errore_held_karp.append(round((peso_held_karp[i] - sol_ottime[i])/sol_ottime[i],3))
        errore_held_karp_avanzato.append(calcolo_errore_avanzato(lista_grafi[i], i, sol_ottime, sol_parziale, peso_held_karp))
        errore_euristica.append(round((peso_euristica[i] - sol_ottime[i])/sol_ottime[i],3))
        errore_due_approssimato.append(round((peso_due_approssimato[i] - sol_ottime[i])/sol_ottime[i],3))

        rapporto_euristica.append(round((peso_euristica[i] - sol_ottime[i])/sol_ottime[i],3))
        rapporto_due_approssimato.append(round((peso_due_approssimato[i] - sol_ottime[i])/sol_ottime[i],3))

    #creo tabella da cui prendere i dati
    table = []
    table.append([grafo.name for grafo in lista_grafi])                 #table[0]
    
    table.append([peso for peso in peso_held_karp])                     #table[1]
    table.append([tempo for tempo in tempo_held_karp])                  #table[2]
    table.append([errore for errore in errore_held_karp])               #table[3]
    table.append([errore for errore in errore_held_karp_avanzato])      #table[4]
    
    table.append([peso for peso in peso_euristica])                     #table[5]
    table.append([tempo for tempo in tempo_euristica])                  #table[6]
    table.append([errore for errore in errore_euristica])               #table[7]
    
    table.append([peso for peso in peso_due_approssimato])              #table[8]
    table.append([tempo for tempo in tempo_due_approssimato])           #table[9]
    table.append([errore for errore in errore_due_approssimato])        #table[10]

    #tabella con i valori inseriti
    tabella = []
    for i in range(len(lista_grafi)):
        tabella.append([table[0][i], table[1][i], table[2][i], table[3][i], table[4][i], table[5][i], table[6][i], table[7][i], table[8][i], table[9][i],table[10][i], min_reloaded([pesoHkNorm[i],tempoHkNorm[i], pesoClosestNorm[i],tempoClosestNorm[i], pesoApproxNorm[i],tempoApproxNorm[i]], i)])

    print()
    print(tabulate(tabella, headers= ["istanza", "peso held karp", "tempo held karp", "errore held karp", "errore hk avanzato", "peso euristica", "tempo euristica", "errore euristica", "peso due approssimato", "tempo due approssimato", "errore due approssimato", "algoritmo migliore"], tablefmt='pretty'))
    plotGraph(rapporto_euristica, rapporto_due_approssimato)








