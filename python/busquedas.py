"""
Algoritmos de búsqueda del Punto 2 (misma estructura que Busquedas.java).

Todos reciben una lista ORDENADA ascendente (salvo la lineal) y devuelven el
índice de la clave o -1 si no está. Versiones iterativas.

Fuentes base (GeeksforGeeks), verificar que los enlaces sigan vigentes:
  Lineal:        https://www.geeksforgeeks.org/linear-search/
  Binaria:       https://www.geeksforgeeks.org/binary-search/
  Ternaria:      https://www.geeksforgeeks.org/ternary-search/
  Saltos:        https://www.geeksforgeeks.org/jump-search/
  Interpolación: https://www.geeksforgeeks.org/interpolation-search/
  Exponencial:   https://www.geeksforgeeks.org/exponential-search/
"""
from math import isqrt


def lineal(a, clave):
    for i in range(len(a)):
        if a[i] == clave:
            return i
    return -1


def _binaria_rango(a, clave, lo, hi):
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if a[mid] == clave:
            return mid
        if a[mid] < clave:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binaria(a, clave):
    return _binaria_rango(a, clave, 0, len(a) - 1)


def ternaria(a, clave):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        tercio = (hi - lo) // 3
        m1 = lo + tercio
        m2 = hi - tercio
        if a[m1] == clave:
            return m1
        if a[m2] == clave:
            return m2
        if clave < a[m1]:
            hi = m1 - 1
        elif clave > a[m2]:
            lo = m2 + 1
        else:
            lo = m1 + 1
            hi = m2 - 1
    return -1


def saltos(a, clave):
    n = len(a)
    if n == 0:
        return -1
    paso = max(1, isqrt(n))
    previo = 0
    actual = paso
    while a[min(actual, n) - 1] < clave:
        previo = actual
        actual += paso
        if previo >= n:
            return -1
    fin = min(actual, n)
    for i in range(previo, fin):
        if a[i] == clave:
            return i
        if a[i] > clave:
            return -1
    return -1


def interpolacion(a, clave):
    lo, hi = 0, len(a) - 1
    while lo <= hi and a[lo] <= clave <= a[hi]:
        if a[hi] == a[lo]:                      # evita división por cero
            return lo if a[lo] == clave else -1
        pos = lo + ((clave - a[lo]) * (hi - lo)) // (a[hi] - a[lo])
        if a[pos] == clave:
            return pos
        if a[pos] < clave:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


def exponencial(a, clave):
    n = len(a)
    if n == 0:
        return -1
    if a[0] == clave:
        return 0
    i = 1
    while i < n and a[i] <= clave:
        i *= 2
    return _binaria_rango(a, clave, i // 2, min(i, n - 1))


ALGORITMOS = [
    ("Lineal", lineal),
    ("Binaria", binaria),
    ("Ternaria", ternaria),
    ("Saltos", saltos),
    ("Interpolacion", interpolacion),
    ("Exponencial", exponencial),
]
