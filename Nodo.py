import math
class Nodo:
    def __init__(self, nodo, padre = None, size = 0, key = 0, in_h = 1, heapIndex = 0):
        self.nodo = nodo
        self.padre = padre  # padre del nodo (str)
        self.size = size    # utile per union-find
        self.key = key      # utile per heap
        self.in_h = in_h    # = 1 perchè tutti i nodi sono nell'heap (prim)
        self.heapIndex = heapIndex      # indice del nodo all'interno dell'heap
    
