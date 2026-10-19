"""Medición de tiempos del taller (lenguaje interpretado: Python).

Uso:  python3 python/experimentos.py [ordenamiento|busqueda|todo] [n1,n2,...]

Mismas reglas que java/src/Experimentos.java:
  - Los datos se leen de datos/*.txt antes de medir; la lectura no entra en el tiempo.
  - time.perf_counter_ns(), 5 repeticiones, promedio y desviación estándar (muestral).
  - CPython no tiene JIT, así que no se hace ejecución de calentamiento.
  - Ordenamiento: cada repetición trabaja sobre una copia nueva; la copia no se mide.
    Después de cada repetición (fuera del tiempo) se verifica que quedó ordenado.
  - Si el tiempo previsto de UNA ejecución supera 5 minutos, no se ejecuta: se estima
    a partir del tamaño anterior y de la complejidad teórica, y se marca "estimado".
  - Si la ejecución falla (RecursionError), se documenta y se estima.
    Se deja el límite de recursión por defecto de Python (1000) a propósito.
"""
import csv
import math
import statistics
import sys
import time
from pathlib import Path

import busqueda as bq
import ordenamiento as od

RAIZ = Path(__file__).resolve().parent.parent
REPS = 5
LIMITE_NS = 300e9  # 5 minutos
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
VARIANTES = ["aleatorio", "asc", "desc"]
LENGUAJE = "Python"

ORDENAMIENTOS = [
    ("Insertion Sort", od.insertion_sort),
    ("Dual-Pivot QuickSort", od.dual_pivot_quick_sort),
    ("Merge Sort", od.merge_sort),
    ("Heap Sort", od.heap_sort),
    ("Radix Sort", od.radix_sort),
    ("Bucket Sort", od.bucket_sort),
]

BUSQUEDAS = [
    ("Lineal", bq.lineal),
    ("Binaria", bq.binaria),
    ("Ternaria", bq.ternaria),
    ("Saltos", bq.saltos),
    ("Interpolacion", bq.interpolacion),
    ("Exponencial", bq.exponencial),
]

CABECERA = ["algoritmo", "lenguaje", "punto", "variante", "n", "t1_ns", "t2_ns", "t3_ns",
            "t4_ns", "t5_ns", "promedio_ns", "desv_ns", "tipo", "nota"]


def modelo(alg, variante):
    """Complejidad que se usa para estimar: 'n', 'nlogn' o 'n2'."""
    if alg == "Insertion Sort":
        return "n" if variante == "asc" else "n2"
    if alg == "Dual-Pivot QuickSort":
        return "nlogn" if variante == "aleatorio" else "n2"
    if alg in ("Radix Sort", "Bucket Sort"):
        return "n"
    return "nlogn"


def g(mod, n):
    if mod == "n":
        return n
    if mod == "n2":
        return n * n
    return n * math.log2(n)


def leer(nombre):
    with open(RAIZ / "datos" / nombre) as f:
        return [int(linea) for linea in f if linea.strip()]


def fila_medida(alg, punto, variante, n, t, nota):
    return [alg, LENGUAJE, punto, variante, n, *[f"{v:.1f}" for v in t],
            f"{statistics.mean(t):.1f}", f"{statistics.stdev(t):.1f}", "medido", nota]


def fila_estimada(alg, punto, variante, n, est, nota):
    return [alg, LENGUAJE, punto, variante, n, "", "", "", "", "", f"{est:.1f}", "", "estimado", nota]


# ----------------------------------------------------------------- Punto 1

def ordenamiento(tamanos):
    with open(RAIZ / "resultados" / "ordenamiento_python.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CABECERA)
        ultimo, fallo = {}, {}
        for n in tamanos:
            for variante in VARIANTES:
                original = leer(f"{variante}_{n}.txt")
                for nombre, fn in ORDENAMIENTOS:
                    clave = (nombre, variante)
                    mod = modelo(nombre, variante)
                    prev = ultimo.get(clave)
                    previsto = 0 if prev is None else prev[1] * g(mod, n) / g(mod, prev[0])

                    if clave in fallo or previsto > LIMITE_NS:
                        motivo = fallo.get(clave, f"previsto {previsto / 1e9:.0f} s > 5 min")
                        nota = f"no ejecutado ({motivo}); estimado desde n={prev[0]} con modelo {mod}"
                        w.writerow(fila_estimada(nombre, "ordenamiento", variante, n, previsto, nota))
                        f.flush()
                        print(f"{nombre:22} {variante:9} n={n:<8} ESTIMADO {previsto / 1e9:.3f} s", flush=True)
                        continue

                    t = []
                    try:
                        for _ in range(REPS):
                            copia = original.copy()
                            t0 = time.perf_counter_ns()
                            fn(copia)
                            t1 = time.perf_counter_ns()
                            t.append(t1 - t0)
                            if not od.esta_ordenado(copia):
                                raise RuntimeError(f"{nombre} no ordenó correctamente")
                    except RecursionError:
                        motivo = (f"RecursionError: se superó el límite de recursión de Python "
                                  f"({sys.getrecursionlimit()})")
                        fallo[clave] = motivo
                        if prev is None:
                            w.writerow([nombre, LENGUAJE, "ordenamiento", variante, n,
                                        "", "", "", "", "", "", "", "error", motivo])
                        else:
                            nota = f"{motivo}; estimado desde n={prev[0]} con modelo {mod}"
                            w.writerow(fila_estimada(nombre, "ordenamiento", variante, n, previsto, nota))
                        f.flush()
                        print(f"{nombre:22} {variante:9} n={n:<8} FALLO ({motivo})", flush=True)
                        continue
                    w.writerow(fila_medida(nombre, "ordenamiento", variante, n, t, "verificado"))
                    f.flush()
                    ultimo[clave] = (n, statistics.mean(t))
                    print(f"{nombre:22} {variante:9} n={n:<8} {statistics.mean(t) / 1e9:.6f} s "
                          f"(desv {statistics.stdev(t) / 1e9:.6f})", flush=True)


# ----------------------------------------------------------------- Punto 2

def medir_busquedas(fn, arr, claves):
    """Devuelve, por repetición, el tiempo promedio por búsqueda en ns."""
    t = []
    for _ in range(REPS):
        t0 = time.perf_counter_ns()
        for c in claves:
            fn(arr, c)
        t1 = time.perf_counter_ns()
        t.append((t1 - t0) / len(claves))
    return t


def verificar(nombre, fn, arr, claves):
    """Fuera del tiempo medido: cada resultado debe ser correcto."""
    existentes = set(arr)
    for c in claves:
        i = fn(arr, c)
        if (c in existentes and (i < 0 or arr[i] != c)) or (c not in existentes and i != -1):
            raise RuntimeError(f"{nombre} falló con la clave {c}")


def busqueda(tamanos):
    with open(RAIZ / "resultados" / "busqueda_python.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CABECERA)
        for n in tamanos:
            arr = leer(f"asc_{n}.txt")
            claves = leer(f"claves_{n}.txt")
            pos = leer(f"clave_pos_{n}.txt")
            for nombre, fn in BUSQUEDAS:
                verificar(nombre, fn, arr, claves)
                t = medir_busquedas(fn, arr, claves)
                w.writerow(fila_medida(nombre, "busqueda", "claves", n, t,
                                       "tiempo promedio por busqueda (total de 1000 / 1000)"))
                print(f"{nombre:14} claves  n={n:<8} {statistics.mean(t):.1f} ns/busqueda", flush=True)
                for etiqueta, clave in zip(["inicio", "centro", "final"], pos):
                    tp = medir_busquedas(fn, arr, [clave] * 1000)
                    w.writerow(fila_medida(nombre, "busqueda", etiqueta, n, tp,
                                           "tiempo promedio por busqueda (1000 veces la misma clave)"))
                f.flush()


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"
    tamanos = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else TAMANOS
    (RAIZ / "resultados").mkdir(exist_ok=True)
    if modo in ("ordenamiento", "todo"):
        ordenamiento(tamanos)
    if modo in ("busqueda", "todo"):
        busqueda(tamanos)


if __name__ == "__main__":
    main()
