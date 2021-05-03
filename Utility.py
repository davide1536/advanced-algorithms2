#from Nodo import *
#from Grafo import *
import math
from heap import heap, HeapDecreaseKey, HeapExtractMin, BuildMinHeap, isIn

h = []


#funzione per convertire le coordinate in radianti
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
    #radice.padre = radice.id
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
        #g.totPeso += u.key
        for i,peso_adj in enumerate(g.adj_matrix[u.id][1:], 1):      #recupero i pesi dei nodi adiacenti ad u 
            if i != u.id: #qui considero  tutti i vicini del nodo u tranne u stesso
                if isIn(g.getNodo(i)) == 1 and peso_adj < g.getNodo(i).key:
                    g.getNodo(i).padre = u
                    index = g.getNodo(i).heapIndex  #ottengo la sua posizione all'interno dell'heap
                    HeapDecreaseKey(q, index, peso_adj)
    return g



def getTree(g):
    for nodo in g.lista_nodi:
        if nodo.padre != None:
            nodo.padre.figlio.append(nodo)



def preOrderVisit(nodo):
    h.append(nodo)
    for figlio in nodo.figlio:
        preOrderVisit(figlio)
    return h
         


