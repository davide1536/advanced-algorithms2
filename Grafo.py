from Nodo import Nodo

class Grafo:
    def __init__(self):
        self.n_nodi = 0
        self.name = None
        self.g_type = None
        self.comment = None
        self.edge_weigt_type = None
        self.edge_weigt_format = None
        self.display_data_type = None 
        self.lista_nodi = []
        self.lista_id_nodi = []
        self.adj_matrix = {} #matrice di adiacenza nxn 
        self.id2Node = {}
        self.diz_pesi = {}      #vettore d[v,S]
        self.diz_padri = {}     #vettore π[v,S]

    
    #restituisce l'oggetto nodo, dato l'id 
    def getNodo(self, id_nodo):
        return self.id2Node[id_nodo]


    #restituisce la lista di oggetti nodi di un grafo
    def getListaNodi(self):
        return list(self.id2Node.values())

    
    