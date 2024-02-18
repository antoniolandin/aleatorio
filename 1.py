# Description: Listar todos los árboles enraizados no isomorfos de N vértices
# Author: Antonio Cabrera

import itertools
import networkx as nx
import matplotlib.pyplot as plt

def isomorfos(arbol1, arbol2):
    n = len(arbol1)
    for i in range(n):
        for j in range(n):
            if arbol1[i][j] != arbol2[i][j]:
                return False
    return True

def es_arbol(arbol):
    n = len(arbol)
    for i in range(n):
        if sum(arbol[i]) != 1:
            return False
    return True

def arboles(n):
    arboles = []
    for arbol in itertools.permutations(range(n)):
        arbol = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    arbol[i][j] = 1
        arboles.append(arbol)
    return arboles

def plot_arbol(arbol, nombre_archivo):
    G = nx.Graph()
    n = len(arbol)
    for i in range(n):
        for j in range(n):
            if arbol[i][j] == 1:
                G.add_edge(i, j)
    nx.draw(G, with_labels=True)
    plt.savefig(nombre_archivo)

if __name__ == "__main__":
    n = 3
    arboles_n = arboles(n)
    for arbol in arboles_n:
        plot_arbol(arbol, f"arbol_{n}.png")
