"""Genera las 9 gráficas y las tablas del informe a partir de resultados/*.csv.

Uso:  python3 python/graficas.py

Convenciones (enunciado del taller):
  - Eje del tiempo siempre en escala logarítmica.
  - Valores estimados: línea punteada y marcador hueco (líneas) o barra rayada (barras).
  - En los gráficos de barras el valor de tiempo va escrito sobre cada barra.
"""
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
GRAF = RAIZ / "graficas"
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
SORTS = ["Insertion Sort", "Dual-Pivot QuickSort", "Merge Sort", "Heap Sort", "Radix Sort", "Bucket Sort"]
SEARCHES = ["Lineal", "Binaria", "Ternaria", "Saltos", "Interpolacion", "Exponencial"]
COLORES = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b"]
VARIANTES = [("aleatorio", "Aleatoria"), ("asc", "Ascendente"), ("desc", "Descendente")]


def cargar():
    datos = {}
    for archivo in ["ordenamiento_java.csv", "ordenamiento_python.csv", "busqueda_java.csv", "busqueda_python.csv"]:
        with open(RES / archivo, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                prom = float(r["promedio_ns"]) if r["promedio_ns"] else None
                desv = float(r["desv_ns"]) if r["desv_ns"] else None
                datos[(r["algoritmo"], r["lenguaje"], r["variante"], int(r["n"]))] = (prom, desv, r["tipo"], r["nota"])
    return datos


def fmt(ns):
    """Tiempo legible a partir de nanosegundos."""
    if ns is None:
        return "error"
    if ns < 1e3:
        return f"{ns:.0f} ns"
    if ns < 1e6:
        return f"{ns / 1e3:.1f} µs"
    if ns < 1e9:
        return f"{ns / 1e6:.2f} ms"
    if ns < 60e9:
        return f"{ns / 1e9:.2f} s"
    if ns < 3600e9:
        return f"{ns / 60e9:.1f} min"
    return f"{ns / 3600e9:.1f} h"


def nota_estimado(ax):
    ax.plot([], [], "k--", marker="o", mfc="white", label="estimado (punteado)")


def lineas(datos, algoritmos, lenguaje, variante, titulo, ylabel, archivo):
    fig, ax = plt.subplots(figsize=(9, 6))
    for alg, color in zip(algoritmos, COLORES):
        puntos = [(n, datos.get((alg, lenguaje, variante, n))) for n in TAMANOS]
        puntos = [(n, d) for n, d in puntos if d and d[0] is not None]
        med = [(n, d[0]) for n, d in puntos if d[2] == "medido"]
        est = [(n, d[0]) for n, d in puntos if d[2] == "estimado"]
        if med:
            ax.plot(*zip(*med), "-o", color=color, label=alg)
        if est:
            enlace = ([med[-1]] if med else []) + est
            ax.plot(*zip(*enlace), "--", color=color)
            ax.plot(*zip(*est), "o", color=color, mfc="white")
    nota_estimado(ax)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (tamaño del arreglo)")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_xticks(TAMANOS, ["1.000", "10.000", "100.000", "1.000.000"])
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(GRAF / archivo, dpi=150)
    plt.close(fig)


def barras(ax, grupos, series, valores, tipos, colores):
    """valores[i][j]: serie j en grupo i (ns). tipos igual, con 'estimado' para rayar."""
    k = len(series)
    ancho = 0.8 / k
    for j, (serie, color) in enumerate(zip(series, colores)):
        for i in range(len(grupos)):
            v, t = valores[i][j], tipos[i][j]
            x = i + (j - (k - 1) / 2) * ancho
            if v is None:
                ax.text(x, ax.get_ylim()[0] * 1.5 if ax.get_yscale() == "log" else 0, "error",
                        ha="center", va="bottom", rotation=90, fontsize=7, color="red")
                continue
            est = t == "estimado"
            ax.bar(x, v, ancho, color="white" if est else color, edgecolor=color,
                   hatch="///" if est else None, linewidth=1.2,
                   label=serie if i == 0 else None)
            ax.text(x, v * 1.15, fmt(v) + (" (est.)" if est else ""), ha="center", va="bottom",
                    rotation=90, fontsize=7)
    ax.set_xticks(range(len(grupos)), grupos, rotation=15, fontsize=9)
    ax.set_yscale("log")


def grafica_barras(grupos, series, valores, tipos, titulo, ylabel, archivo, colores):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    vals = [v for fila in valores for v in fila if v]
    ax.set_yscale("log")
    ax.set_ylim(min(vals) / 3, max(vals) * 60)
    barras(ax, grupos, series, valores, tipos, colores)
    ax.bar(0, 0, 0, color="white", edgecolor="gray", hatch="///", label="estimado (rayado)")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.grid(True, axis="y", which="both", alpha=0.3)
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout()
    fig.savefig(GRAF / archivo, dpi=150)
    plt.close(fig)


def tabla(encabezado, filas):
    out = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    out += ["| " + " | ".join(str(c) for c in f) + " |" for f in filas]
    return "\n".join(out)


def celda(d):
    if d is None:
        return "—"
    if d[0] is None:
        return "error"
    texto = fmt(d[0])
    if d[2] == "estimado":
        return f"*{texto} (est.)*"
    return f"{texto} ± {fmt(d[1])}" if d[1] is not None else texto


def teorico(mod):
    return {"n": "10", "nlogn": "≈ 13,3 / 12,5 / 12", "n2": "100"}[mod]


def main():
    GRAF.mkdir(exist_ok=True)
    d = cargar()

    # ---------------- Punto 1
    for lang in ["Java", "Python"]:
        lineas(d, SORTS, lang, "aleatorio", f"Ordenamiento – crecimiento ({lang}, entrada aleatoria)",
               "tiempo promedio (ns, escala log)", f"p1_crecimiento_{lang.lower()}.png")
    for n in [1_000, 10_000, 100_000]:
        vals = [[(d.get((a, "Java", v, n)) or (None,))[0] for v, _ in VARIANTES] for a in SORTS]
        tips = [[(d.get((a, "Java", v, n)) or (None, None, ""))[2] for v, _ in VARIANTES] for a in SORTS]
        grafica_barras(SORTS, [e for _, e in VARIANTES], vals, tips,
                       "Efecto del orden de entrada – Java, n = " + f"{n:,}".replace(",", "."),
                       "tiempo promedio (ns, escala log)", f"p1_orden_entrada_{n}.png",
                       ["#1f77b4", "#2ca02c", "#d62728"])
    vals = [[(d.get((a, l, "aleatorio", 1_000_000)) or (None,))[0] for l in ["Java", "Python"]] for a in SORTS]
    tips = [[(d.get((a, l, "aleatorio", 1_000_000)) or (None, None, ""))[2] for l in ["Java", "Python"]] for a in SORTS]
    grafica_barras(SORTS, ["Java", "Python"], vals, tips,
                   "Ordenamiento – compilado vs interpretado (n = 1.000.000, aleatoria)",
                   "tiempo promedio (ns, escala log)", "p1_java_vs_python.png", ["#1f77b4", "#ff7f0e"])

    # ---------------- Punto 2
    for lang in ["Java", "Python"]:
        lineas(d, SEARCHES, lang, "claves", f"Búsqueda – crecimiento ({lang}, 1.000 claves)",
               "tiempo promedio por búsqueda (ns, escala log)", f"p2_crecimiento_{lang.lower()}.png")
    vals = [[d[(a, l, "claves", 1_000_000)][0] for l in ["Java", "Python"]] for a in SEARCHES]
    tips = [["medido"] * 2 for _ in SEARCHES]
    grafica_barras(SEARCHES, ["Java", "Python"], vals, tips,
                   "Búsqueda – compilado vs interpretado (n = 1.000.000)",
                   "tiempo promedio por búsqueda (ns, escala log)", "p2_java_vs_python.png",
                   ["#1f77b4", "#ff7f0e"])

    # ---------------- Tablas (Markdown) para el informe
    md = ["# Tablas generadas a partir de resultados/*.csv", "",
          "Valores: promedio ± desviación estándar de 5 repeticiones. *(est.)* = estimado, no ejecutado.", ""]
    for lang in ["Java", "Python"]:
        for v, nombre in VARIANTES:
            md += [f"## Ordenamiento – {lang} – entrada {nombre.lower()}", ""]
            md.append(tabla(["Algoritmo"] + [f"n={n:,}".replace(",", ".") for n in TAMANOS],
                            [[a] + [celda(d.get((a, lang, v, n))) for n in TAMANOS] for a in SORTS]))
            md.append("")
    md += ["## Factor de crecimiento T(10n)/T(n), entrada aleatoria", "",
           "Teórico: O(n) → 10; O(n log n) → 13,3 (1k→10k), 12,5 (10k→100k), 12 (100k→1M); O(n²) → 100.", ""]
    from experimentos import modelo  # noqa: E402
    filas = []
    for lang in ["Java", "Python"]:
        for a in SORTS:
            fila = [a, lang]
            for n1, n2 in zip(TAMANOS, TAMANOS[1:]):
                x, y = d.get((a, lang, "aleatorio", n1)), d.get((a, lang, "aleatorio", n2))
                if x and y and x[0] and y[0]:
                    marca = " (est.)" if "estimado" in (x[2], y[2]) else ""
                    fila.append(f"{y[0] / x[0]:.1f}{marca}")
                else:
                    fila.append("—")
            fila.append(teorico(modelo(a, "aleatorio")))
            filas.append(fila)
    md.append(tabla(["Algoritmo", "Lenguaje", "1k→10k", "10k→100k", "100k→1M", "Teórico"], filas))
    md.append("")
    for lang in ["Java", "Python"]:
        md += [f"## Búsqueda – {lang} – tiempo promedio por búsqueda (1.000 claves)", ""]
        md.append(tabla(["Algoritmo"] + [f"n={n:,}".replace(",", ".") for n in TAMANOS],
                        [[a] + [celda(d.get((a, lang, "claves", n))) for n in TAMANOS] for a in SEARCHES]))
        md.append("")
    for lang in ["Java", "Python"]:
        md += [f"## Posición de la clave – {lang} – n = 1.000.000 (tiempo promedio por búsqueda)", ""]
        md.append(tabla(["Algoritmo", "Inicio", "Centro", "Final"],
                        [[a] + [celda(d.get((a, lang, p, 1_000_000))) for p in ["inicio", "centro", "final"]]
                         for a in SEARCHES]))
        md.append("")
    (RES / "tablas.md").write_text("\n".join(md), encoding="utf-8")
    print("listo:", sorted(p.name for p in GRAF.glob("*.png")))


if __name__ == "__main__":
    main()
