from Arco import Arco
from Nodo import Nodo
import copy
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
        self.totPeso = 0
        self.diz_pesi = {}      #vettore d[v,S]
        self.diz_padri = {}     #vettore π[v,S]
        self.id2NodeSet = {}
        
    
       
    
    """ def aggiungiArco(self, arco):
        self.n_archi += 1
        arco_inverso = Arco(arco.nodo2, arco.nodo1, arco.peso)
        self.lista_archi.append(arco)
        self.lista_archi.append(arco_inverso)
        
        self.lista_adiacenza[arco.nodo2].append(arco_inverso) #aggiungo arco inverso al nodo già presente nel grafo
        self.lista_adiacenza[arco.nodo1].append(arco) 
        
        self.lista_adiacenza_nodi[arco.nodo2].append(self.getNodo(arco.nodo1)) #aggiungo il nuovo nodo alla lista dei vicini del nodo2
        self.lista_adiacenza_nodi[arco.nodo1].append(self.getNodo(arco.nodo2)) #agginugno il nodo2 alla lista dei vicini del nuovo nodo """

    
    #restituisce l'oggetto nodo, dato l'id 
    def getNodo(self, id_nodo):
        return self.id2Node[id_nodo]

    #creo un id basato su v, S (precisamente una stringa [[v], [S]]) 
    #in modo da poter estrarre i valori dal dizionario id -> peso o id -> padri
    def getNodeSet(self, v, S):
        v = [v]
        v.append(S)
        return self.id2NodeSet[str(v)]

    #restituisce la lista di oggetti nodi di un grafo
    def getListaNodi(self):
        return list(self.id2Node.values())

    
    