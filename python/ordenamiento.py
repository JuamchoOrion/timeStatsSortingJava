"""Algoritmos de ordenamiento del Punto 1.

Fuente principal: GeeksforGeeks (la URL de cada algoritmo está en su comentario).
Es una traducción línea a línea de java/src/Ordenamiento.java, para que ambos
lenguajes ejecuten exactamente la misma implementación.
"""


# ---------------------------------------------------------------
# Insertion Sort
# https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
# ---------------------------------------------------------------
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ---------------------------------------------------------------
# Dual-Pivot QuickSort (pivotes: primer y último elemento)
# https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/
# ---------------------------------------------------------------
def dual_pivot_quick_sort(arr):
    _dual_pivot_quick_sort(arr, 0, len(arr) - 1)


def _dual_pivot_quick_sort(arr, low, high):
    if low < high:
        lp, rp = _partition(arr, low, high)
        _dual_pivot_quick_sort(arr, low, lp - 1)
        _dual_pivot_quick_sort(arr, lp + 1, rp - 1)
        _dual_pivot_quick_sort(arr, rp + 1, high)


def _partition(arr, low, high):
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    j = low + 1
    g, k = high - 1, low + 1
    p, q = arr[low], arr[high]
    while k <= g:
        if arr[k] < p:
            arr[k], arr[j] = arr[j], arr[k]
            j += 1
        elif arr[k] >= q:
            while arr[g] > q and k < g:
                g -= 1
            arr[k], arr[g] = arr[g], arr[k]
            g -= 1
            if arr[k] < p:
                arr[k], arr[j] = arr[j], arr[k]
                j += 1
        k += 1
    j -= 1
    g += 1
    arr[low], arr[j] = arr[j], arr[low]
    arr[high], arr[g] = arr[g], arr[high]
    return j, g


# ---------------------------------------------------------------
# Merge Sort
# https://www.geeksforgeeks.org/dsa/merge-sort/
# ---------------------------------------------------------------
def merge_sort(arr):
    _merge_sort(arr, 0, len(arr) - 1)


def _merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m)
        _merge_sort(arr, m + 1, r)
        _merge(arr, l, m, r)


def _merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = arr[l:l + n1]
    R = arr[m + 1:m + 1 + n2]
    i = j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


# ---------------------------------------------------------------
# Heap Sort
# https://www.geeksforgeeks.org/dsa/heap-sort/
# ---------------------------------------------------------------
def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)


# Versión iterativa del heapify de GfG (misma lógica, sin recursión de cola)
def _heapify(arr, n, i):
    while True:
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest == i:
            return
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


# ---------------------------------------------------------------
# Radix Sort (LSD, base 10, counting sort estable por dígito)
# https://www.geeksforgeeks.org/dsa/radix-sort/
# ---------------------------------------------------------------
def radix_sort(arr):
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
    for i in range(n - 1, -1, -1):
        d = (arr[i] // exp) % 10
        output[count[d] - 1] = arr[i]
        count[d] -= 1
    arr[:] = output


# ---------------------------------------------------------------
# Bucket Sort para enteros
# https://www.geeksforgeeks.org/dsa/bucket-sort-2/
# Se usan n cubetas. El valor x va a la cubeta
#     idx = (x - min) * n // (max - min + 1)
# de modo que el rango [min, max] se parte en n intervalos de igual ancho.
# Cada cubeta se ordena con Insertion Sort (como en GfG) y luego se concatenan.
# ---------------------------------------------------------------
def bucket_sort(arr):
    n = len(arr)
    if n == 0:
        return
    mn = mx = arr[0]
    for v in arr:
        if v < mn:
            mn = v
        if v > mx:
            mx = v
    rango = mx - mn + 1
    buckets = [[] for _ in range(n)]
    for v in arr:
        idx = (v - mn) * n // rango
        buckets[idx].append(v)
    k = 0
    for b in buckets:
        insertion_sort(b)
        for v in b:
            arr[k] = v
            k += 1


def esta_ordenado(arr):
    for i in range(1, len(arr)):
        if arr[i - 1] > arr[i]:
            return False
    return True
