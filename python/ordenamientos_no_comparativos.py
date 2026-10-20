"""
Algoritmos de ordenamiento NO basados en comparaciones (Rol 2). Ambos ordenan IN SITU una lista de enteros.
Misma estructura que java/NoComparativos.java (mismos nombres y mismo enfoque).

Fuentes (GeeksforGeeks, completar con la fecha de consulta):
  - Radix Sort:   https://www.geeksforgeeks.org/radix-sort/
  - Bucket Sort:  https://www.geeksforgeeks.org/bucket-sort-2/
"""


# ---------------------------------------------------------------- Radix Sort
def radix_sort(arr):
    """LSD en base 10: una pasada de Counting Sort estable por dígito (8 pasadas con 8 dígitos).
    En Python los enteros no tienen tamaño fijo, así que la misma función sirve para 16 dígitos."""
    n = len(arr)
    if n == 0:
        return
    mx = arr[0]
    for v in arr:
        if v > mx:
            mx = v
    output = [0] * n
    exp = 1
    while mx // exp > 0:
        _count_sort(arr, output, n, exp)
        exp *= 10


def _count_sort(arr, output, n, exp):
    count = [0] * 10
    for i in range(n):
        count[(arr[i] // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):          # de atrás hacia adelante: mantiene la estabilidad
        d = (arr[i] // exp) % 10
        output[count[d] - 1] = arr[i]
        count[d] -= 1
    arr[:] = output                         # equivale a System.arraycopy en Java


# ---------------------------------------------------------------- Bucket Sort
def bucket_sort(arr):
    """k = n cubetas; el valor x va a la cubeta idx = (x - min) * k // (max - min + 1), siempre en [0, k-1].
    Cada cubeta se ordena con Insertion Sort (estable) y luego se concatenan."""
    n = len(arr)
    if n == 0:
        return
    mn = mx = arr[0]
    for v in arr:
        if v < mn:
            mn = v
        if v > mx:
            mx = v
    k = n
    rango = mx - mn + 1
    cubetas = [[] for _ in range(k)]
    for v in arr:
        cubetas[(v - mn) * k // rango].append(v)
    pos = 0
    for c in cubetas:
        _insertion_sort_cubeta(c)
        for v in c:
            arr[pos] = v
            pos += 1


def _insertion_sort_cubeta(c):
    for i in range(1, len(c)):
        key = c[i]
        j = i - 1
        while j >= 0 and c[j] > key:
            c[j + 1] = c[j]
            j -= 1
        c[j + 1] = key
