"""Algoritmos de búsqueda del Punto 2. Todos devuelven el índice de x o -1.

Fuente principal: GeeksforGeeks (la URL de cada algoritmo está en su comentario).
Es una traducción línea a línea de java/src/Busqueda.java.
"""
import math


# https://www.geeksforgeeks.org/dsa/linear-search/
def lineal(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1


# https://www.geeksforgeeks.org/dsa/binary-search/ (versión iterativa)
def binaria(arr, x, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# https://www.geeksforgeeks.org/dsa/ternary-search/ (versión iterativa)
def ternaria(arr, x):
    l, r = 0, len(arr) - 1
    while r >= l:
        mid1 = l + (r - l) // 3
        mid2 = r - (r - l) // 3
        if arr[mid1] == x:
            return mid1
        if arr[mid2] == x:
            return mid2
        if x < arr[mid1]:
            r = mid1 - 1
        elif x > arr[mid2]:
            l = mid2 + 1
        else:
            l = mid1 + 1
            r = mid2 - 1
    return -1


# https://www.geeksforgeeks.org/dsa/jump-search/  (salto = raíz de n)
def saltos(arr, x):
    n = len(arr)
    step = math.floor(math.sqrt(n))
    prev = 0
    while arr[min(step, n) - 1] < x:
        prev = step
        step += math.floor(math.sqrt(n))
        if prev >= n:
            return -1
    while arr[prev] < x:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[prev] == x:
        return prev
    return -1


# https://www.geeksforgeeks.org/dsa/interpolation-search/
# Se protege la división cuando arr[hi] == arr[lo] (valores repetidos).
def interpolacion(arr, x):
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= x <= arr[hi]:
        if arr[hi] == arr[lo]:
            return lo if arr[lo] == x else -1
        pos = lo + ((hi - lo) * (x - arr[lo])) // (arr[hi] - arr[lo])
        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


# https://www.geeksforgeeks.org/dsa/exponential-search/
def exponencial(arr, x):
    n = len(arr)
    if arr[0] == x:
        return 0
    i = 1
    while i < n and arr[i] <= x:
        i = i * 2
    return binaria(arr, x, i // 2, min(i, n - 1))
