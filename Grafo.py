from Arco import Arco
from Nodo import Nodo
import copy
class Grafo:
    def __init__(self):
        self.n_nodi = 0
        self.n_archi = 0
        self.lista_nodi = set()
        self.lista_archi = []
        self.id2Node = {}
        self.lista_adiacenza = {} #dizionario key: nodo (str), value: lista archi del nodo (obj arco)
        self.lista_adiacenza_nodi = {} #dizionario key: nodo (str), value: lista nodi adiacenti (obj nodo)
        self.totPeso = 0
    
       
    
    def aggiungiArco(self, arco):
        self.n_archi += 1
        arco_inverso = Arco(arco.nodo2, arco.nodo1, arco.peso)
        self.lista_archi.append(arco)
        self.lista_archi.append(arco_inverso)
        
        self.lista_adiacenza[arco.nodo2].append(arco_inverso) #aggiungo arco inverso al nodo già presente nel grafo
        self.lista_adiacenza[arco.nodo1].append(arco) 
        
        self.lista_adiacenza_nodi[arco.nodo2].append(self.getNodo(arco.nodo1)) #aggiungo il nuovo nodo alla lista dei vicini del nodo2
        self.lista_adiacenza_nodi[arco.nodo1].append(self.getNodo(arco.nodo2)) #agginugno il nodo2 alla lista dei vicini del nuovo nodo

    
    #restituisce l'oggetto nodo, dato l'id 
    def getNodo(self, id_nodo):
        return self.id2Node[id_nodo]

    #restituisce la lista di oggetti nodi di un grafo
    def getListaNodi(self):
        return list(self.id2Node.values())


    #mostra vettore dei padri
    def getGrafoPrim(self):
        g = Grafo()
        lista_adiacenza_nodi_padri = {}
        numero_archi = 0
        for nodo in self.getListaNodi():
            lista_adiacenza_nodi_padri.setdefault(nodo.nodo, [])
        for nodo in self.id2Node.values():
            if nodo.nodo != nodo.padre:
                numero_archi += 1
                lista_adiacenza_nodi_padri[nodo.nodo].append(self.getNodo(nodo.padre))
                lista_adiacenza_nodi_padri[nodo.padre].append(self.getNodo(nodo.nodo))
        
        g.lista_adiacenza_nodi = lista_adiacenza_nodi_padri
        g.n_archi = numero_archi
        g.n_nodi = len(lista_adiacenza_nodi_padri.keys())
        g.id2Node = copy.deepcopy(self.id2Node)
        g.totPeso = self.totPeso

        return g

    

    def printAdj(self):
        for i in self.lista_adiacenza_nodi.keys():
            print(i, [arco.getArco()[1] for arco in self.lista_adiacenza[i]])
       
    