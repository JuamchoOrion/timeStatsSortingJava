"""
Mediciones del Punto 2 (búsqueda) en Python.

Uso (desde la raíz del repo):
    python python/medir_busqueda.py                    # todos los tamaños
    python python/medir_busqueda.py --tamanos 1000,10000   # solo esos (pruebas)

Escribe resultados/busqueda_python.csv con el esquema acordado:
    algoritmo,lenguaje,variante,n,t1_ns..t5_ns,promedio_ns,desviacion_ns,tipo,observacion
Cada t_i es el tiempo PROMEDIO POR BÚSQUEDA (ns) de la repetición i.

Si UNA repetición supera LIMITE_SEG (5 min), se aborta esa configuración y se
registra una fila 'estimado' extrapolando linealmente desde el tamaño anterior
(solo tiene sentido para la búsqueda lineal, que es O(n)).
"""
import argparse
import csv
import statistics
import time
from bisect import bisect_left
from pathlib import Path

from busquedas import ALGORITMOS

REPETICIONES = 5
VECES_POSICION = 1000
LIMITE_SEG = 300
RAIZ = Path(__file__).resolve().parent.parent
sumidero = 0  # acumula resultados para que el trabajo de búsqueda no sea "inútil"


def leer(ruta):
    with open(ruta) as f:
        return [int(x) for x in f if x.strip()]


def verificar(nombre, alg, arr, claves):
    """Verificación FUERA del tiempo medido (contra bisect)."""
    for c in claves:
        r = alg(arr, c)
        i = bisect_left(arr, c)
        presente = i < len(arr) and arr[i] == c
        if presente and (r < 0 or arr[r] != c):
            raise AssertionError(f"{nombre} no encontró {c}")
        if not presente and r != -1:
            raise AssertionError(f"{nombre} devolvió índice para clave ausente {c}")


def medir(escritor, nombre, variante, n, alg, arr, claves, previos):
    """Una configuración: 5 repeticiones, cada una busca todas las claves."""
    global sumidero
    t = []
    for _ in range(REPETICIONES):
        suma = 0
        t0 = time.perf_counter_ns()
        for c in claves:
            suma += alg(arr, c)
        t1 = time.perf_counter_ns()
        sumidero += suma
        dur = t1 - t0
        t.append(dur / len(claves))
        if dur / 1e9 > LIMITE_SEG:
            clave_prev = (nombre, variante)
            if clave_prev in previos:
                n_prev, t_prev = previos[clave_prev]
                est = t_prev * n / n_prev
                escritor.writerow([nombre, "python", variante, n, "", "", "", "", "",
                                   f"{est:.3f}", "", "estimado",
                                   f"una repetición superó {LIMITE_SEG}s; extrapolado O(n) desde n={n_prev}"])
                print(f"  {nombre:<14} {variante:<26} ESTIMADO {est:,.0f} ns/búsqueda")
                return
            print(f"  {nombre} {variante}: superó el límite y no hay tamaño previo para estimar")
            return
    prom = statistics.mean(t)
    desv = statistics.stdev(t)
    escritor.writerow([nombre, "python", variante, n] + [f"{x:.3f}" for x in t] +
                      [f"{prom:.3f}", f"{desv:.3f}", "medido", ""])
    previos[(nombre, variante)] = (n, prom)
    print(f"  {nombre:<14} {variante:<26} {prom:12.1f} ns/búsqueda")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tamanos", default="1000,10000,100000,1000000")
    ap.add_argument("--raiz", default=str(RAIZ))
    args = ap.parse_args()
    raiz = Path(args.raiz)
    tamanos = [int(x) for x in args.tamanos.split(",")]
    (raiz / "resultados").mkdir(exist_ok=True)
    salida = raiz / "resultados" / "busqueda_python.csv"
    previos = {}

    with open(salida, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["algoritmo", "lenguaje", "variante", "n", "t1_ns", "t2_ns", "t3_ns", "t4_ns",
                    "t5_ns", "promedio_ns", "desviacion_ns", "tipo", "observacion"])
        for n in tamanos:
            asc = leer(raiz / "datos" / f"asc_{n}.txt")
            claves = leer(raiz / "datos" / f"claves_{n}.txt")
            print(f"n = {n}")
            for nombre, alg in ALGORITMOS:
                verificar(nombre, alg, asc, claves)
                medir(w, nombre, "claves_mixtas", n, alg, asc, claves, previos)
                f.flush()
            if n == 1_000_000:
                inicio, centro, final = leer(raiz / "datos" / f"clave_pos_{n}.txt")
                for nombre, alg in ALGORITMOS:
                    for var, clave in (("pos_inicio", inicio), ("pos_centro", centro), ("pos_final", final)):
                        medir(w, nombre, var, n, alg, asc, [clave] * VECES_POSICION, previos)
                        f.flush()
                # Lineal sobre el arreglo DESORDENADO (insumo del Punto 3.2).
                desord = leer(raiz / "datos" / f"aleatorio_{n}.txt")
                medir(w, "Lineal", "claves_mixtas_desordenado", n, ALGORITMOS[0][1], desord, claves, previos)
                f.flush()
    print(f"Listo: {salida}  (sumidero={sumidero})")


if __name__ == "__main__":
    main()
