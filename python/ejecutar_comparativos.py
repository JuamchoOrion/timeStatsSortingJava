"""
Uso (desde la raíz del repo):
    python python/ejecutar_comparativos.py                  # todo (4 algoritmos x 3 variantes)
    python python/ejecutar_comparativos.py merge asc        # una sola configuración
Algoritmos: insertion, dualpivot, merge, heap.  Variantes: aleatorio, asc, desc.
"""
import sys

import arnes
from ordenamientos_comparativos import insertion_sort, dual_pivot_quicksort, merge_sort, heap_sort

# nombre en CSV, función, modelo de complejidad por variante (solo para estimar)
ALGORITMOS = {
    "insertion": ("Insertion Sort", insertion_sort, {"aleatorio": "n2", "asc": "n", "desc": "n2"}),
    "dualpivot": ("Dual-Pivot QuickSort", dual_pivot_quicksort, {"aleatorio": "nlogn", "asc": "n2", "desc": "n2"}),
    "merge": ("Merge Sort", merge_sort, {"aleatorio": "nlogn", "asc": "nlogn", "desc": "nlogn"}),
    "heap": ("Heap Sort", heap_sort, {"aleatorio": "nlogn", "asc": "nlogn", "desc": "nlogn"}),
}
VARIANTES = ["aleatorio", "asc", "desc"]

if __name__ == "__main__":
    algs = [sys.argv[1]] if len(sys.argv) > 1 else list(ALGORITMOS)
    vars_ = [sys.argv[2]] if len(sys.argv) > 2 else VARIANTES
    for a in algs:
        nombre, fn, modelos = ALGORITMOS[a]
        for v in vars_:
            arnes.correr(nombre, fn, v, modelos[v])
