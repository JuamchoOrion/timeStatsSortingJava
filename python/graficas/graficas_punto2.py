"""
Gráficas y tablas del Punto 2 (búsqueda).

Uso (desde la raíz del repo, después de correr las mediciones de Java y Python):
    python python/graficas/graficas_punto2.py

Lee resultados/busqueda*.csv y genera en graficas/:
    crecimiento_busqueda_java.png, crecimiento_busqueda_python.png   (log-log)
    comparacion_busqueda_1000000.png                                (barras, Java vs Python)
y en resultados/ las tablas de posición de la clave:
    tabla_posicion_java.csv/.md, tabla_posicion_python.csv/.md

Reglas del taller: eje del tiempo logarítmico; estimados con línea punteada o
barra rayada; valor del tiempo visible sobre cada barra.
"""
import argparse
import unicodedata
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

RAIZ = Path(__file__).resolve().parents[2]
LENGUAJE_COMPILADO = "java"
LENGUAJE_INTERPRETADO = "python"
N_GRANDE = 1_000_000

NOMBRES = {"lineal": "Lineal", "binaria": "Binaria", "ternaria": "Ternaria",
           "saltos": "Saltos (Jump)", "interpolacion": "Interpolación", "exponencial": "Exponencial"}
ORDEN = list(NOMBRES.values())
COLORES = dict(zip(ORDEN, plt.cm.tab10.colors))
MARCADORES = dict(zip(ORDEN, ["o", "s", "^", "D", "v", "P"]))
COLOR_LENG = {LENGUAJE_COMPILADO: "#1f77b4", LENGUAJE_INTERPRETADO: "#ff7f0e"}


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def cargar(resultados):
    archivos = sorted(Path(resultados).glob("busqueda*.csv"))
    if not archivos:
        raise SystemExit(f"No hay archivos busqueda*.csv en {resultados}")
    df = pd.concat([pd.read_csv(a) for a in archivos], ignore_index=True)
    df["lenguaje"] = df["lenguaje"].str.strip().str.lower()
    df["variante"] = df["variante"].str.strip().str.lower()
    df["tipo"] = df["tipo"].str.strip().str.lower()
    clave = df["algoritmo"].map(lambda s: sin_tildes(str(s)).lower().split()[0].split("(")[0])
    df["alg"] = clave.map(NOMBRES)
    df = df[df["alg"].notna() & df["tipo"].isin(["medido", "estimado"])].copy()
    df["n"] = df["n"].astype(int)
    df["promedio_ns"] = df["promedio_ns"].astype(float)
    return df


def fmt_ns(ns):
    if ns < 1e3:
        return f"{ns:.0f} ns"
    if ns < 1e6:
        return f"{ns / 1e3:.1f} µs"
    if ns < 1e9:
        return f"{ns / 1e6:.1f} ms"
    return f"{ns / 1e9:.2f} s"


def grafica_crecimiento(df, lenguaje, salida):
    sub = df[(df.lenguaje == lenguaje) & (df.variante == "claves_mixtas")]
    if sub.empty:
        print(f"  (sin datos de {lenguaje}, se omite el crecimiento)")
        return
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for alg in ORDEN:
        s = sub[sub.alg == alg].sort_values("n")
        if s.empty:
            continue
        xs, ys, est = s["n"].to_numpy(), s["promedio_ns"].to_numpy(), (s["tipo"] == "estimado").to_numpy()
        for i in range(len(xs) - 1):
            ax.plot(xs[i:i + 2], ys[i:i + 2], color=COLORES[alg],
                    linestyle="--" if (est[i] or est[i + 1]) else "-", linewidth=1.8)
        for x, y, e in zip(xs, ys, est):
            ax.plot(x, y, marker=MARCADORES[alg], color=COLORES[alg],
                    markerfacecolor="white" if e else COLORES[alg], markersize=7)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamaño del arreglo n (escala log)")
    ax.set_ylabel("Tiempo promedio por búsqueda (ns, escala log)")
    ax.set_title(f"Búsqueda: crecimiento del tiempo con n ({lenguaje.capitalize()}, claves mixtas)")
    ax.grid(True, which="both", alpha=0.3)
    h = [Line2D([0], [0], color=COLORES[a], marker=MARCADORES[a], label=a) for a in ORDEN if (sub.alg == a).any()]
    h += [Line2D([0], [0], color="k", linestyle="-", label="Medido"),
          Line2D([0], [0], color="k", linestyle="--", marker="o", markerfacecolor="white", label="Estimado")]
    ax.legend(handles=h, loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(salida, dpi=200)
    plt.close(fig)
    print("  ->", salida)


def grafica_comparacion(df, salida):
    sub = df[(df.n == N_GRANDE) & (df.variante == "claves_mixtas")]
    langs = [l for l in (LENGUAJE_COMPILADO, LENGUAJE_INTERPRETADO) if (sub.lenguaje == l).any()]
    if len(langs) < 2:
        print("  (faltan datos de n=1.000.000 en alguno de los lenguajes, se omite la comparación)")
        return
    algs = [a for a in ORDEN if (sub.alg == a).any()]
    valores = {(a, l): sub[(sub.alg == a) & (sub.lenguaje == l)].iloc[0] for a in algs for l in langs
               if not sub[(sub.alg == a) & (sub.lenguaje == l)].empty}
    ymin = min(v["promedio_ns"] for v in valores.values()) / 3
    ymax = max(v["promedio_ns"] for v in valores.values()) * 60
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    ancho = 0.38
    x = np.arange(len(algs))
    for j, l in enumerate(langs):
        for i, a in enumerate(algs):
            if (a, l) not in valores:
                continue
            v = valores[(a, l)]
            est = v["tipo"] == "estimado"
            xb = x[i] + (j - 0.5) * ancho
            ax.bar(xb, v["promedio_ns"] - ymin, ancho, bottom=ymin, color=COLOR_LENG[l],
                   hatch="//" if est else None, edgecolor="black", linewidth=0.6)
            ax.text(xb, v["promedio_ns"] * 1.12, fmt_ns(v["promedio_ns"]) + (" (est.)" if est else ""),
                    ha="center", va="bottom", fontsize=7.5, rotation=90)
    ax.set_yscale("log")
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(x)
    ax.set_xticklabels(algs)
    ax.set_ylabel("Tiempo promedio por búsqueda (ns, escala log)")
    ax.set_title("Búsqueda con n = 1.000.000: compilado vs interpretado (claves mixtas)")
    ax.grid(True, axis="y", which="both", alpha=0.3)
    ax.legend(handles=[Patch(facecolor=COLOR_LENG[l], label=l.capitalize()) for l in langs] +
                      [Patch(facecolor="white", edgecolor="black", hatch="//", label="Estimado")], loc="upper right")
    fig.tight_layout()
    fig.savefig(salida, dpi=200)
    plt.close(fig)
    print("  ->", salida)


def tabla_posicion(df, lenguaje, carpeta):
    sub = df[(df.lenguaje == lenguaje) & (df.n == N_GRANDE) & df.variante.isin(["pos_inicio", "pos_centro", "pos_final"])]
    if sub.empty:
        print(f"  (sin datos de posición para {lenguaje})")
        return
    filas = []
    for a in ORDEN:
        fila = {"Algoritmo": a}
        for var, col in (("pos_inicio", "Inicio"), ("pos_centro", "Centro"), ("pos_final", "Final")):
            s = sub[(sub.alg == a) & (sub.variante == var)]
            fila[col] = "" if s.empty else s.iloc[0]["promedio_ns"]
            fila[col + "_tipo"] = "" if s.empty else s.iloc[0]["tipo"]
        filas.append(fila)
    t = pd.DataFrame(filas)
    t.to_csv(Path(carpeta) / f"tabla_posicion_{lenguaje}.csv", index=False)
    lineas = [f"Tiempo promedio por búsqueda (ns), n = 1.000.000, {lenguaje.capitalize()}", "",
              "| Algoritmo | Inicio | Centro | Final |", "|---|---|---|---|"]
    for _, f in t.iterrows():
        celdas = []
        for col in ("Inicio", "Centro", "Final"):
            celdas.append("" if f[col] == "" else f"{f[col]:,.1f}" + (" (est.)" if f[col + "_tipo"] == "estimado" else ""))
        lineas.append(f"| {f['Algoritmo']} | " + " | ".join(celdas) + " |")
    (Path(carpeta) / f"tabla_posicion_{lenguaje}.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas), "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resultados", default=str(RAIZ / "resultados"))
    ap.add_argument("--salida", default=str(RAIZ / "graficas"))
    a = ap.parse_args()
    Path(a.salida).mkdir(parents=True, exist_ok=True)
    df = cargar(a.resultados)
    print("Gráficas de crecimiento")
    for l in (LENGUAJE_COMPILADO, LENGUAJE_INTERPRETADO):
        grafica_crecimiento(df, l, Path(a.salida) / f"crecimiento_busqueda_{l}.png")
    print("Comparación compilado vs interpretado")
    grafica_comparacion(df, Path(a.salida) / f"comparacion_busqueda_{N_GRANDE}.png")
    print("Tablas de posición de la clave")
    for l in (LENGUAJE_COMPILADO, LENGUAJE_INTERPRETADO):
        tabla_posicion(df, l, a.resultados)


if __name__ == "__main__":
    main()
