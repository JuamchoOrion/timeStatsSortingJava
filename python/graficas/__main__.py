"""
Módulo común de gráficas (Rol 2; Rol 3 lo reutiliza para el Punto 2).

Uso (desde la raíz del repo):
    python -m pip install matplotlib
    python python/graficas

Lee los CSV de resultados/ (esquema común del grupo) y genera en graficas/ las gráficas que pueda,
según qué CSV existan:
  Punto 1 (ordenamiento_comparativos.csv + ordenamiento_no_comparativos.csv):
    p1_crecimiento_java.png, p1_crecimiento_python.png,
    p1_orden_entrada_1000.png, p1_orden_entrada_10000.png, p1_orden_entrada_100000.png,
    p1_java_vs_python.png
  Punto 2 (busqueda.csv):
    p2_crecimiento_java.png, p2_crecimiento_python.png, p2_java_vs_python.png
Además escribe resultados/tablas.md con las tablas para el informe (incluida la de factores T(10n)/T(n)
y las de posición de la clave).

Reglas (sección 2.7 del documento de roles): eje del tiempo en escala log (ambos ejes en las de
crecimiento); estimados con línea punteada y marcador hueco, o barra rayada; valor sobre cada barra.
"""
import csv
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(RAIZ, "resultados")
GRAF = os.path.join(RAIZ, "graficas")
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
ETIQUETAS_N = ["1.000", "10.000", "100.000", "1.000.000"]
ORDENAMIENTOS = ["Insertion Sort", "Dual-Pivot QuickSort", "Merge Sort", "Heap Sort", "Radix Sort", "Bucket Sort"]
BUSQUEDAS = ["Lineal", "Binaria", "Ternaria", "Saltos", "Interpolacion", "Exponencial"]
COLORES = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b"]
VARIANTES = [("aleatorio", "Aleatoria"), ("asc", "Ascendente"), ("desc", "Descendente")]
CSV_P1 = ["ordenamiento_comparativos.csv", "ordenamiento_no_comparativos.csv"]
CSV_P2 = ["busqueda_java.csv", "busqueda_python.csv"]


def cargar(archivos):
    """{(algoritmo, lenguaje, variante, n): (promedio_ns | None, desviacion_ns | None, tipo, observacion)}.
    Si una configuración aparece repetida (por ejemplo, se corrió dos veces), gana la última fila."""
    datos = {}
    for nombre in archivos:
        ruta = os.path.join(RES, nombre)
        if not os.path.exists(ruta):
            continue
        with open(ruta, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                prom = float(r["promedio_ns"]) if r["promedio_ns"] else None
                desv = float(r["desviacion_ns"]) if r["desviacion_ns"] else None
                datos[(r["algoritmo"], r["lenguaje"].strip().capitalize(), r["variante"], int(r["n"]))] = (
                    prom, desv, r["tipo"], r["observacion"])
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


def guardar(fig, archivo):
    os.makedirs(GRAF, exist_ok=True)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAF, archivo), dpi=150)
    plt.close(fig)
    print("graficas/" + archivo)


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
            ax.plot(*zip(*enlace), "--", color=color, label=None if med else alg)
            ax.plot(*zip(*est), "o", color=color, mfc="white")
    ax.plot([], [], "k--", marker="o", mfc="white", label="estimado (punteado)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (tamaño del arreglo)")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_xticks(TAMANOS, ETIQUETAS_N)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9)
    guardar(fig, archivo)


def barras(grupos, series, valores, tipos, titulo, ylabel, archivo, colores):
    """valores[i][j]: tiempo (ns) de la serie j en el grupo i; tipos[i][j] = 'medido' | 'estimado'."""
    fig, ax = plt.subplots(figsize=(11, 6.5))
    vals = [v for fila in valores for v in fila if v]
    if not vals:
        plt.close(fig)
        return
    ax.set_yscale("log")
    ax.set_ylim(min(vals) / 3, max(vals) * 60)
    k = len(series)
    ancho = 0.8 / k
    for j, (serie, color) in enumerate(zip(series, colores)):
        for i in range(len(grupos)):
            v, t = valores[i][j], tipos[i][j]
            x = i + (j - (k - 1) / 2) * ancho
            if v is None:
                ax.text(x, min(vals) / 2.5, "sin dato", ha="center", va="bottom", rotation=90, fontsize=7, color="red")
                continue
            est = t == "estimado"
            ax.bar(x, v, ancho, color="white" if est else color, edgecolor=color,
                   hatch="///" if est else None, linewidth=1.2, label=serie if i == 0 else None)
            ax.text(x, v * 1.15, fmt(v) + (" (est.)" if est else ""), ha="center", va="bottom",
                    rotation=90, fontsize=7)
    ax.bar(0, 0, 0, color="white", edgecolor="gray", hatch="///", label="estimado (rayado)")
    ax.set_xticks(range(len(grupos)), grupos, rotation=15, fontsize=9)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.grid(True, axis="y", which="both", alpha=0.3)
    ax.legend(fontsize=9, loc="upper right")
    guardar(fig, archivo)


def valor(d, clave):
    x = d.get(clave)
    return (x[0], x[2]) if x else (None, "")


def tabla(encabezado, filas):
    out = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    out += ["| " + " | ".join(str(c) for c in f) + " |" for f in filas]
    return "\n".join(out)


def celda(x):
    if x is None:
        return "—"
    if x[0] is None:
        return "error"
    if x[2] == "estimado":
        return f"*{fmt(x[0])} (est.)*"
    return f"{fmt(x[0])} ± {fmt(x[1])}" if x[1] is not None else fmt(x[0])


def modelo(alg, variante):
    if alg == "Insertion Sort":
        return "n" if variante == "asc" else "n2"
    if alg == "Dual-Pivot QuickSort":
        return "nlogn" if variante == "aleatorio" else "n2"
    if alg in ("Radix Sort", "Bucket Sort"):
        return "n"
    return "nlogn"


def razon_teorica(mod, n1, n2):
    if mod == "n":
        return n2 / n1
    if mod == "n2":
        return (n2 / n1) ** 2
    return (n2 * math.log2(n2)) / (n1 * math.log2(n1))


def punto1(d, md):
    for lang in ["Java", "Python"]:
        lineas(d, ORDENAMIENTOS, lang, "aleatorio", f"Ordenamiento – crecimiento ({lang}, entrada aleatoria)",
               "tiempo promedio (ns, escala log)", f"p1_crecimiento_{lang.lower()}.png")
    for n, etiqueta in zip(TAMANOS[:3], ETIQUETAS_N[:3]):
        celdas = [[valor(d, (a, "Java", v, n)) for v, _ in VARIANTES] for a in ORDENAMIENTOS]
        barras(ORDENAMIENTOS, [e for _, e in VARIANTES], [[c[0] for c in f] for f in celdas],
               [[c[1] for c in f] for f in celdas], f"Efecto del orden de entrada – Java, n = {etiqueta}",
               "tiempo promedio (ns, escala log)", f"p1_orden_entrada_{n}.png", ["#1f77b4", "#2ca02c", "#d62728"])
    celdas = [[valor(d, (a, l, "aleatorio", 1_000_000)) for l in ["Java", "Python"]] for a in ORDENAMIENTOS]
    barras(ORDENAMIENTOS, ["Java", "Python"], [[c[0] for c in f] for f in celdas], [[c[1] for c in f] for f in celdas],
           "Ordenamiento – compilado vs interpretado (n = 1.000.000, entrada aleatoria)",
           "tiempo promedio (ns, escala log)", "p1_java_vs_python.png", ["#1f77b4", "#ff7f0e"])

    for lang in ["Java", "Python"]:
        for v, nombre in VARIANTES:
            md += [f"## Ordenamiento – {lang} – entrada {nombre.lower()}", ""]
            md.append(tabla(["Algoritmo"] + [f"n={e}" for e in ETIQUETAS_N],
                            [[a] + [celda(d.get((a, lang, v, n))) for n in TAMANOS] for a in ORDENAMIENTOS]))
            md.append("")
    md += ["## Factor de crecimiento T(10n)/T(n), entrada aleatoria", "",
           "Entre paréntesis, la razón que predice la complejidad teórica. *(est.)* = usa un valor estimado.", ""]
    filas = []
    for lang in ["Java", "Python"]:
        for a in ORDENAMIENTOS:
            fila = [a, lang]
            for n1, n2 in zip(TAMANOS, TAMANOS[1:]):
                x, y = d.get((a, lang, "aleatorio", n1)), d.get((a, lang, "aleatorio", n2))
                teo = razon_teorica(modelo(a, "aleatorio"), n1, n2)
                if x and y and x[0] and y[0]:
                    marca = " (est.)" if "estimado" in (x[2], y[2]) else ""
                    fila.append(f"{y[0] / x[0]:.1f}{marca} ({teo:.1f})")
                else:
                    fila.append(f"— ({teo:.1f})")
            filas.append(fila)
    md.append(tabla(["Algoritmo", "Lenguaje", "1k→10k", "10k→100k", "100k→1M"], filas))
    md.append("")
    filas = []
    for a in ORDENAMIENTOS:
        j, p = d.get((a, "Java", "aleatorio", 1_000_000)), d.get((a, "Python", "aleatorio", 1_000_000))
        razon = f"{p[0] / j[0]:.1f}" if j and p and j[0] and p[0] else "—"
        filas.append([a, celda(j), celda(p), razon])
    md += ["## Compilado vs interpretado – ordenamiento, n = 1.000.000, entrada aleatoria", ""]
    md.append(tabla(["Algoritmo", "Java", "Python", "Python / Java"], filas))
    md.append("")


def punto2(d, md):
    for lang in ["Java", "Python"]:
        lineas(d, BUSQUEDAS, lang, "claves_mixtas", f"Búsqueda – crecimiento ({lang}, 1.000 claves mixtas)",
               "tiempo promedio por búsqueda (ns, escala log)", f"p2_crecimiento_{lang.lower()}.png")
    celdas = [[valor(d, (a, l, "claves_mixtas", 1_000_000)) for l in ["Java", "Python"]] for a in BUSQUEDAS]
    barras(BUSQUEDAS, ["Java", "Python"], [[c[0] for c in f] for f in celdas], [[c[1] for c in f] for f in celdas],
           "Búsqueda – compilado vs interpretado (n = 1.000.000)",
           "tiempo promedio por búsqueda (ns, escala log)", "p2_java_vs_python.png", ["#1f77b4", "#ff7f0e"])
    for lang in ["Java", "Python"]:
        md += [f"## Búsqueda – {lang} – tiempo promedio por búsqueda (1.000 claves mixtas)", ""]
        md.append(tabla(["Algoritmo"] + [f"n={e}" for e in ETIQUETAS_N],
                        [[a] + [celda(d.get((a, lang, "claves_mixtas", n))) for n in TAMANOS] for a in BUSQUEDAS]))
        md.append("")
    for lang in ["Java", "Python"]:
        md += [f"## Posición de la clave – {lang} – n = 1.000.000 (tiempo promedio por búsqueda)", ""]
        md.append(tabla(["Algoritmo", "Inicio", "Centro", "Final"],
                        [[a] + [celda(d.get((a, lang, p, 1_000_000))) for p in ["pos_inicio", "pos_centro", "pos_final"]]
                         for a in BUSQUEDAS]))
        md.append("")


def main():
    md = ["# Tablas generadas a partir de resultados/*.csv", "",
          "Promedio ± desviación estándar muestral de 5 repeticiones. *(est.)* = estimado.", ""]
    d1 = cargar(CSV_P1)
    if d1:
        punto1(d1, md)
    else:
        print("No hay CSV del Punto 1 todavía; se omiten sus gráficas.")
    d2 = cargar(CSV_P2)
    if d2:
        punto2(d2, md)
    else:
        print("No hay resultados/busqueda.csv todavía; se omiten las gráficas del Punto 2.")
    with open(os.path.join(RES, "tablas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("resultados/tablas.md")


if __name__ == "__main__":
    main()
