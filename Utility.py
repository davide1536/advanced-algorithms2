#from Nodo import *
#from Grafo import *
import math

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
