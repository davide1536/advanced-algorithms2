#from Nodo import *
#from Grafo import *
import math
from heap import *
#funzione per convertire le coordinate in radianti
def convert(x):
    PI = 3.141592
    #deg = round(x)
    deg = int(x)
    min = x - deg
    rad = round(PI * (deg + 5.0 * min/3.0) // 180.0)
    #rad = round(PI * (deg + 5.0 * min/3.0) // 180.0)
    return rad

def calcGeoDist(nodo1, nodo2):
    RRR = 6378.388
    q1 = math.cos(nodo1.x - nodo2.x)
    q2 = math.cos(nodo1.y - nodo2.y)
    q3 = math.cos(nodo1.y + nodo2.y)
    dist = (int) (RRR * math.acos(0.5*((1.0 + q1)*q2 - (1.0 - q1)*q3)) + 1.0)
    return dist

def calcEuclDist(nodo1, nodo2):
    dist = round(math.sqrt((nodo1.x - nodo2.x)**2 + (nodo1.y - nodo2.y)**2))
    return dist

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
                u.figlio = nodo_adj.nodo
                index = nodo_adj.heapIndex  #ottengo la sua posizione all'interno dell'heap
                HeapDecreaseKey(q, index, arco.peso)
    return g
def preOrderVisit(nodo):
    h = []
    h.append(radice)
    if nodo.figlio != None:
        for figlio in nodo.figlio:
            preOrderVisit(nodo) 
    return h


