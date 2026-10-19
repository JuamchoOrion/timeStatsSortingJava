"""
Arnés de medición para ORDENAMIENTO. Rol 2 lo reutiliza con `correr(...)`.

- Lee datos/<variante>_<n>.txt (fuera del tiempo medido).
- Cada repetición usa una COPIA nueva (fuera del tiempo medido).
- Cronometra solo la llamada al algoritmo con time.perf_counter_ns().
- Verifica el orden fuera del tiempo medido.
- Captura RecursionError y tiempo excedido (>300 s, solo Linux/macOS) y escribe una fila ESTIMADA.
- Desviación estándar MUESTRAL (n-1).
"""
import csv
import math
import os
import signal
import statistics
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "datos")
CSV_RUTA = os.path.join(RAIZ, "resultados", "ordenamiento_comparativos.csv")
TAMANOS = [1000, 10000, 100000, 1000000]
REPS = 5
LIMITE_S = 300
ENCABEZADO = ["algoritmo", "lenguaje", "variante", "n", "t1_ns", "t2_ns", "t3_ns", "t4_ns",
              "t5_ns", "promedio_ns", "desviacion_ns", "tipo", "observacion"]
NOMBRE_MODELO = {"n2": "O(n^2)", "n": "O(n)", "nlogn": "O(n log n)"}


class Fallo(Exception):
    def __init__(self, tipo, mensaje):
        super().__init__(mensaje)
        self.tipo = tipo
        self.mensaje = mensaje


class _Excedido(Exception):
    pass


def _alarma(signum, frame):
    raise _Excedido()


def leer(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return [int(x) for x in f.read().replace(",", " ").split()]


def factor(modelo, n):
    if modelo == "n2":
        return float(n) * n
    if modelo == "n":
        return float(n)
    return n * math.log2(n)


def cronometrar(algoritmo, original):
    copia = list(original)                       # copia FUERA del tiempo
    usa_alarma = hasattr(signal, "setitimer")
    if usa_alarma:
        signal.signal(signal.SIGALRM, _alarma)
        signal.setitimer(signal.ITIMER_REAL, LIMITE_S)
    try:
        ini = time.perf_counter_ns()
        algoritmo(copia)
        t = time.perf_counter_ns() - ini
    except RecursionError:
        raise Fallo("RECURSION", "RecursionError")
    except _Excedido:
        raise Fallo("TIMEOUT", f"excedió {LIMITE_S} s")
    finally:
        if usa_alarma:
            signal.setitimer(signal.ITIMER_REAL, 0)
    if copia != sorted(original):                # verificación FUERA del tiempo
        raise Fallo("ERROR", "el arreglo no quedó ordenado")
    return t


def escribir_fila(fila):
    os.makedirs(os.path.dirname(CSV_RUTA), exist_ok=True)
    nuevo = not os.path.exists(CSV_RUTA) or os.path.getsize(CSV_RUTA) == 0
    with open(CSV_RUTA, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        if nuevo:
            w.writerow(ENCABEZADO)
        w.writerow(fila)


def correr(nombre, algoritmo, variante, modelo, lenguaje="Python"):
    """Mide un algoritmo en una variante para todos los tamaños. modelo: 'n2' | 'n' | 'nlogn'
    (complejidad a usar SOLO para estimar si el caso no termina o falla)."""
    t0, n0, causa = None, None, None
    for n in TAMANOS:
        if causa is not None:
            _estimado(nombre, lenguaje, variante, n, modelo, t0, n0, causa)
            continue
        datos = leer(f"{variante}_{n}.txt")
        try:
            ts = [cronometrar(algoritmo, datos) for _ in range(REPS)]
        except Fallo as e:
            causa = f"{e.tipo}: {e.mensaje} en n={n}"
            print(f"[{lenguaje}] {nombre} {variante} n={n}: {causa}")
            _estimado(nombre, lenguaje, variante, n, modelo, t0, n0, causa)
            continue
        prom = statistics.mean(ts)
        desv = statistics.stdev(ts)
        escribir_fila([nombre, lenguaje, variante, n, *ts, f"{prom:.1f}", f"{desv:.1f}", "medido", ""])
        print(f"[{lenguaje}] {nombre} {variante} n={n}: {prom/1e6:.3f} ms (±{desv/1e6:.3f})")
        t0, n0 = prom, n


def _estimado(nombre, lenguaje, variante, n, modelo, t0, n0, causa):
    if t0 is None:
        prom, obs = "", f"{causa}; sin medición previa para extrapolar"
    else:
        prom = f"{t0 * factor(modelo, n) / factor(modelo, n0):.1f}"
        obs = f"{causa}; extrapolado con {NOMBRE_MODELO[modelo]} desde n={n0}"
    escribir_fila([nombre, lenguaje, variante, n, "", "", "", "", "", prom, "", "estimado", obs])
