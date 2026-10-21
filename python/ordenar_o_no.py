"""
Punto 3.2 - ¿Ordenar o no ordenar?

Calcula a partir de qué número de búsquedas k conviene ordenar el arreglo
(con el mejor algoritmo de ordenamiento medido) y luego usar búsqueda binaria,
en lugar de hacer k búsquedas lineales sobre el arreglo desordenado:

    t_ordenar + k * t_binaria  <  k * t_lineal   =>   k > t_ordenar / (t_lineal - t_binaria)

Uso (desde la raíz del repo, con los CSV de ordenamiento y de búsqueda listos):
    python python/ordenar_o_no.py

Toma de resultados/:
  - t_ordenar : menor promedio de ordenamiento*.csv con n = 1.000.000, variante aleatorio
  - t_lineal  : Lineal, variante claves_mixtas_desordenado (n = 1.000.000); si no existe,
                usa Lineal claves_mixtas sobre el arreglo ordenado y lo advierte
  - t_binaria : Binaria, variante claves_mixtas (n = 1.000.000)
Escribe resultados/punto3_2.csv y muestra el cálculo paso a paso.
"""
import argparse
import math
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
N = 1_000_000


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").lower()


def cargar(resultados, patron):
    archivos = sorted(Path(resultados).glob(patron))
    if not archivos:
        raise SystemExit(f"No hay archivos {patron} en {resultados}")
    df = pd.concat([pd.read_csv(a) for a in archivos], ignore_index=True)
    for c in ("lenguaje", "variante", "tipo"):
        df[c] = df[c].astype(str).str.strip().str.lower()
    df["alg"] = df["algoritmo"].map(sin_tildes)
    return df[df["tipo"].isin(["medido", "estimado"])]


def fmt(ns):
    return f"{ns:,.1f} ns  ({ns / 1e6:,.4f} ms)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resultados", default=str(RAIZ / "resultados"))
    a = ap.parse_args()
    orden = cargar(a.resultados, "ordenamiento*.csv")
    busq = cargar(a.resultados, "busqueda*.csv")
    filas = []

    for leng in ("java", "python"):
        print("=" * 70)
        print(f"Lenguaje: {leng}")
        o = orden[(orden.lenguaje == leng) & (orden.n == N) & (orden.variante == "aleatorio")]
        if o.empty:
            print("  Faltan datos de ordenamiento con n = 1.000.000 y entrada aleatoria.")
            continue
        mejor = o.loc[o["promedio_ns"].idxmin()]
        t_ord = float(mejor["promedio_ns"])
        aviso = " (VALOR ESTIMADO)" if mejor["tipo"] == "estimado" else ""

        b = busq[(busq.lenguaje == leng) & (busq.n == N)]
        lin = b[(b.alg == "lineal") & (b.variante == "claves_mixtas_desordenado")]
        nota_lin = "Lineal sobre arreglo desordenado"
        if lin.empty:
            lin = b[(b.alg == "lineal") & (b.variante == "claves_mixtas")]
            nota_lin = "ADVERTENCIA: se usó Lineal sobre el arreglo ORDENADO (justifíquenlo en el informe)"
        bin_ = b[(b.alg == "binaria") & (b.variante == "claves_mixtas")]
        if lin.empty or bin_.empty:
            print("  Faltan datos de búsqueda Lineal/Binaria con n = 1.000.000.")
            continue
        t_lin = float(lin.iloc[0]["promedio_ns"])
        t_bin = float(bin_.iloc[0]["promedio_ns"])

        print(f"  Mejor ordenamiento: {mejor['algoritmo']}{aviso}")
        print(f"  t_ordenar = {fmt(t_ord)}")
        print(f"  t_lineal  = {fmt(t_lin)}   [{nota_lin}]")
        print(f"  t_binaria = {fmt(t_bin)}")
        if t_lin <= t_bin:
            print("  La búsqueda lineal no es más lenta que la binaria: nunca conviene ordenar.")
            k_min = None
        else:
            k_real = t_ord / (t_lin - t_bin)
            k_min = math.ceil(k_real)
            if k_real == k_min:
                k_min += 1  # desigualdad estricta
            print(f"  k > t_ordenar / (t_lineal - t_binaria) = {t_ord:,.1f} / ({t_lin:,.1f} - {t_bin:,.1f}) = {k_real:,.3f}")
            print(f"  => conviene ordenar a partir de k = {k_min:,} búsquedas")
            costo_a = k_min * t_lin
            costo_b = t_ord + k_min * t_bin
            print(f"  Comprobación con k = {k_min:,}: sin ordenar = {costo_a / 1e6:,.3f} ms; ordenando = {costo_b / 1e6:,.3f} ms")
        filas.append({"lenguaje": leng, "algoritmo_ordenamiento": mejor["algoritmo"], "tipo_t_ordenar": mejor["tipo"],
                      "t_ordenar_ns": t_ord, "t_lineal_ns": t_lin, "t_binaria_ns": t_bin, "k_minimo": k_min,
                      "nota_t_lineal": nota_lin})
    if filas:
        salida = Path(a.resultados) / "punto3_2.csv"
        pd.DataFrame(filas).to_csv(salida, index=False)
        print("=" * 70)
        print("Guardado en", salida)


if __name__ == "__main__":
    main()
