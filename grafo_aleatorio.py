from random import random

def random_graph(n, p):
    """
    Devuelve un grafo aleatorio con n vértices y probabilidad p de que haya una arista entre dos vértices
    """
    G = {}
    for i in range(n):
        G[i] = []
        for j in range(n):
            if i != j:
                if random() < p:
                    G[i].append(j)
    return G

def es_conexo(G):
    """
    Devuelve True si el grafo G es conexo, False en caso contrario
    """
    visitados = [False] * len(G)
    visitados[0] = True
    pila = [0]
    while pila:
        v = pila.pop()
        for w in G[v]:
            if not visitados[w]:
                visitados[w] = True
                pila.append(w)
    return all(visitados)

def get_pconexo(n, p):
    """
    Devuelve la probabilidad de que un grafo aleatorio con n vértices y probabilidad p de que haya una arista entre dos vértices sea conexo
    """

    ITERACIONES = 100000

    c = 0
    for _ in range(ITERACIONES):
        G = random_graph(n, p)
        if es_conexo(G):
            c += 1
    return c / ITERACIONES

if __name__ == "__main__":
    n = 6
    p = 0.5
    print(get_pconexo(n, p))
