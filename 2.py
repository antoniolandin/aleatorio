# Description: Para N vértices determinar p para que el grafo aleatorio (p, N) sea conexo ocn la probabilidad PConexo dada, graficar la función f(N)= p | (p, N) conexo con la probabilidad del 50%. Punto adicional por su aproximación analítica. 
# Author: Antonio Cabrera

import math
import matplotlib.pyplot as plt
import time
import scipy
import numpy as np

# Función para determinar PConexo para un grafo aleatorio (p, N)
# Source: https://math.stackexchange.com/questions/584228/exact-probability-of-random-graph-being-connected
def get_pconexo(N, p) -> float:

    # Casos base
    if N == 1:
        return 1
    elif N == 2:
        return p

    sum = 0

    for i in range(1, N):
        sum+=get_pconexo(i, p)*(math.comb(N-1, i-1))*(1 - p)**(i*(N-i))

    return 1-sum

def get_pconexo_my_implementation(N, p) -> float:
    M = math.comb(N, 2)

    number_connected_graphs = 0.0 

    for i in range(N-1, M+1):
        number_connected_graphs += np.multiply(scipy.special.comb(M, i), np.power(p, M, dtype=np.float128))

    return number_connected_graphs

# Clase para obtener PConexo de manera optimizada (recursión con memorización)
class get_pconexo_optimized:
    def __init__(self, N):
        self.N = N
        # Lista para almacenar los valores de PConexo y evitar recálculos
        self.cache = [-1.0]*N # -1 indica que el valor no ha sido calculado
        
    def get_pconexo_recursive(self, N, p) -> float:
        
        # Casos base
        if N == 1:
            return 1
        elif N == 2:
            return p

        # Si el valor ya ha sido calculado, retornar el valor almacenado
        if self.cache[N-1] != -1:
            return self.cache[N-1]
        else:
            sum = 0

            for i in range(1, N):
                sum+=self.get_pconexo_recursive(i,p)*scipy.special.comb(N-1, i-1)*np.power((1-p),(i*(N-i)))

            self.cache[N-1] = 1-sum
            return 1-sum

    def get_pconexo(self, p) -> float:
        self.clear_cache()
        return self.get_pconexo_recursive(self.N, p)

    def clear_cache(self):
        self.cache = [-1.0]*len(self.cache)

# Función para aproximar p para que el grafo aleatorio (p, N) sea conexo con la probabilidad PConexo dada
def get_p(N, pconexo) -> float:
    p = 0
    
    while get_pconexo(N,p) < pconexo:
        p+=0.01

    return p

def get_p_my_implementation(N, pconexo) -> float:
    p = 0
    
    while get_pconexo_my_implementation(N,p) < pconexo:
        p+=0.01

    return p

# Función para aproximar p para que el grafo aleatorio (p, N) sea conexo con la probabilidad PConexo dada de manera optimizada (aproximación con el método de Brent)
def get_p_optimized(N, pconexo) -> float:
    optimized = get_pconexo_optimized(N)
    
    # Creamos una función cuya raíz sea el valor de p que buscamos
    f = lambda p: optimized.get_pconexo(p) - pconexo
    
    # Utilizamos el método de Brent para encontrar la raíz (la probabilidad p que buscamos)
    p = scipy.optimize.brentq(f, 0, 1)

    return p

# Función para aproximar p para que el grafo aleatorio (p, N) sea conexo con la probabilidad PConexo dada de manera optimizada utilizando mi algoritmo para conseguir p (aproximación con el método de Brent)
def get_p_optimized_my_implementation(N, pconexo): 
    # Creamos una función cuya raíz sea el valor de p que buscamos
    f = lambda p: get_pconexo_my_implementation(N, p) - pconexo
    
    # Utilizamos el método de Brent para encontrar la raíz (la probabilidad p que buscamos)
    p = scipy.optimize.brentq(f, 0, 1)

    return p

if __name__ == '__main__':
    DEBUG = -1

    pconexo = 0.5
    n = 40
    n_range = range(2, n)
    
    if DEBUG == 0:
        time_start = time.time()
        f=[get_p(i, pconexo) for i in n_range] 
        total_time = time.time() - time_start

        time_start = time.time()
        f_optimized=[get_p_optimized(i, pconexo) for i in n_range]
        total_time_optimized = time.time() - time_start

        print('Test de rendimiento')
        print(f'Cálculo de PConexo para N=20 y p=0.5')
        print(f'Tiempo total sin optimizar: {total_time} segundos')
        print(f'Tiempo total optimizado: {total_time_optimized} segundos')
        print(f'Optimización: {total_time/total_time_optimized}x')
        
        print('\n----------------------------------------------------------------------------------')

        for i in range(len(n_range)):
            print(f'N={n_range[i]} | f(N)={f[i]} | f_optimized(N)={f_optimized[i]}')

    elif DEBUG == 1:         
        suma = 0 

        for n in n_range:
            f_n = get_p_optimized(n, pconexo)
            optimized = get_pconexo_optimized(n)

            error = abs(optimized.get_pconexo(f_n) - pconexo)
            suma += error

        media = suma/len(n_range)

        print(f'Error medio de la aproximación de p: {media}')

    elif DEBUG == 2:

        pconexo_list = []

        p=0.5

        for n in n_range:
            optimized = get_pconexo_optimized(n)
            pconexo_list.append(optimized.get_pconexo(p))

        plt.plot(n_range, pconexo_list, '--ro', label='StackExchange')
        plt.xlabel('N')
        plt.ylabel('PConexo')
        plt.title(f'PConexo de (p, N) con p={p}')

        # My implementation
        pconexo_list = []
        
        for n in n_range:
            pconexo_list.append(get_pconexo_my_implementation(n, p))

        plt.plot(n_range, pconexo_list, '--bo', label='My implementation')
        plt.legend()
        plt.show()

    elif DEBUG == 3:
       
        start_time = 0 
        sum_time = 0
        sum_time_my_implementation = 0
       
        n_range = range(2, 10)

        for n in n_range:
            print(f'N={n}')

            start_time = time.time()
            print(get_pconexo(n, 0.5))
            sum_time += time.time() - start_time
            
            start_time = time.time()
            print(get_pconexo_my_implementation(n, 0.5))
            sum_time_my_implementation += time.time() - start_time
            print('---')

        print(f'Tiempo medio de get_pconexo: {sum_time/len(n_range)}')
        print(f'Tiempo medio de get_pconexo_my_implementation: {sum_time_my_implementation/len(n_range)}')
    elif DEBUG == 4:

        optimized = get_pconexo_optimized(10)

        f = [optimized.get_pconexo(pconexo) for i in n_range]
        f_my_implementation = [get_pconexo_my_implementation(i, pconexo) for i in n_range]

        for i in range(len(n_range)):
            print(f'N={n_range[i]} | f(N)={f[i]} | f_my_implementation(N)={f_my_implementation[i]}')
    else:
        f = [get_p_optimized(i, pconexo) for i in n_range]   

        plt.plot(n_range, f, '--ro', label='StackExchange (optimized)')
        plt.xlabel('N')
        plt.ylabel('p')
        plt.title(f'f(N) = p | (p, N) conexo con PConexo={pconexo}')

        # f = [get_pconexo(i, pconexo) for i in n_range]
        # plt.plot(n_range, f, '--go', label='StackExchange')
        
        f = [get_p_optimized_my_implementation(i, pconexo) for i in n_range]
        plt.plot(n_range, f, '--bo', label='My implementation')
        plt.legend()
        plt.show()
