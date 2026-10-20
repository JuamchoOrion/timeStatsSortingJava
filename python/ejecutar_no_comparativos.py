"""
Uso (desde la raíz del repo):
    python python/ejecutar_no_comparativos.py                 # todo (2 algoritmos x 3 variantes)
    python python/ejecutar_no_comparativos.py radix asc       # una sola configuración
Algoritmos: radix, bucket.  Variantes: aleatorio, asc, desc.
Reutiliza el arnés del Rol 1 (arnes.correr) y escribe resultados/ordenamiento_no_comparativos.csv
(un CSV por rol, mismo esquema).
"""
import os
import sys

import arnes
from ordenamientos_no_comparativos import radix_sort, bucket_sort

arnes.CSV_RUTA = os.path.join(arnes.RAIZ, "resultados", "ordenamiento_no_comparativos.csv")

# nombre en CSV, función. Ambos son O(n) con estos datos: el modelo "n" solo se usa para estimar.
ALGORITMOS = {
    "radix": ("Radix Sort", radix_sort),
    "bucket": ("Bucket Sort", bucket_sort),
}
VARIANTES = ["aleatorio", "asc", "desc"]

if __name__ == "__main__":
    algs = [sys.argv[1]] if len(sys.argv) > 1 else list(ALGORITMOS)
    vars_ = [sys.argv[2]] if len(sys.argv) > 2 else VARIANTES
    for a in algs:
        nombre, fn = ALGORITMOS[a]
        for v in vars_:
            arnes.correr(nombre, fn, v, "n")
