"""
Algoritmos de ordenamiento por comparación . Todos ordenan IN SITU una lista de enteros.
Misma estructura que java/Ordenamientos.java (mismos nombres y mismo enfoque).

Fuentes (GeeksforGeeks, completar con la fecha de consulta):
  - Insertion Sort:        https://www.geeksforgeeks.org/insertion-sort-algorithm/
  - Dual-Pivot QuickSort:  https://www.geeksforgeeks.org/dual-pivot-quicksort/
  - Merge Sort:            https://www.geeksforgeeks.org/merge-sort/
  - Heap Sort:             https://www.geeksforgeeks.org/heap-sort/
"""


# ---------------------------------------------------------------- Insertion Sort
def insertion_sort(arr):
    """Versión clásica por desplazamientos."""
    for i in range(1, len(arr)):
        k = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > k:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = k


# ---------------------------------------------------------------- Dual-Pivot QuickSort
def dual_pivot_quicksort(arr):
    _dpq(arr, 0, len(arr) - 1)


def _dpq(arr, low, high):
    # Recursivo, SIN modificar el límite de recursión: si falla, se documenta.
    if low < high:
        lp, rp = _particion(arr, low, high)
        _dpq(arr, low, lp - 1)
        _dpq(arr, lp + 1, rp - 1)
        _dpq(arr, rp + 1, high)


def _particion(arr, low, high):
    # Pivotes: primer y último elemento (p <= q).
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    j = low + 1
    g = high - 1
    k = low + 1
    p = arr[low]
    q = arr[high]
    while k <= g:
        if arr[k] < p:                      # zona izquierda (< p)
            arr[k], arr[j] = arr[j], arr[k]
            j += 1
        elif arr[k] >= q:                   # zona derecha (>= q)
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


# ---------------------------------------------------------------- Merge Sort
def merge_sort(arr):
    """Recursivo descendente. El arreglo auxiliar se asigna UNA sola vez."""
    if len(arr) < 2:
        return
    aux = arr[:]
    _ms(arr, aux, 0, len(arr) - 1)


def _ms(arr, aux, lo, hi):
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    _ms(arr, aux, lo, mid)
    _ms(arr, aux, mid + 1, hi)
    aux[lo:hi + 1] = arr[lo:hi + 1]         # equivale a System.arraycopy en Java
    i, j, k = lo, mid + 1, lo
    while i <= mid and j <= hi:
        if aux[i] <= aux[j]:                # <= mantiene la estabilidad
            arr[k] = aux[i]; i += 1
        else:
            arr[k] = aux[j]; j += 1
        k += 1
    while i <= mid:
        arr[k] = aux[i]; i += 1; k += 1
    while j <= hi:
        arr[k] = aux[j]; j += 1; k += 1


# ---------------------------------------------------------------- Heap Sort
def heap_sort(arr):
    """Montículo máximo, construcción + extracción repetida, todo iterativo."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)


def _heapify(arr, n, i):
    while True:
        mayor = i
        l = 2 * i + 1
        r = l + 1
        if l < n and arr[l] > arr[mayor]:
            mayor = l
        if r < n and arr[r] > arr[mayor]:
            mayor = r
        if mayor == i:
            return
        arr[i], arr[mayor] = arr[mayor], arr[i]
        i = mayor
