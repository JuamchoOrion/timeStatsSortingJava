"""
Datos del EXPERIMENTO ADICIONAL del Punto 3.1 (Rol 2). Se generan una sola vez, con semilla propia,
en archivos aparte de los datos oficiales:

  datos/extra_concentrado_100000.txt  100.000 enteros de 8 dígitos NO uniformes: el 99 % cae en un rango
                                      de solo 1.000 valores (50.000.000 a 50.000.999) y el 1 % restante se
                                      reparte en todo el rango de 8 dígitos, así min y max siguen lejos.
  datos/extra_16digitos_100000.txt    100.000 enteros aleatorios de 16 dígitos (10^15 a 10^16 - 1).

Por qué el 1 % disperso: Bucket Sort calcula las cubetas con el min y el max reales. Si todos los
valores estuvieran en un rango pequeño, las cubetas se ajustarían a ese rango y el algoritmo seguiría
siendo rápido. El caso malo es cuando unos pocos valores extremos "estiran" el rango y el resto se amontona.
"""
import random
from pathlib import Path

SEMILLA = 2026
N = 100_000
DATOS = Path(__file__).resolve().parent.parent / "datos"


def guardar(nombre, valores):
    with open(DATOS / nombre, "w") as f:
        f.write("\n".join(map(str, valores)) + "\n")


def main():
    rnd = random.Random(SEMILLA)
    concentrado = [rnd.randint(10_000_000, 99_999_999) if rnd.random() < 0.01
                   else rnd.randint(50_000_000, 50_000_999) for _ in range(N)]
    guardar(f"extra_concentrado_{N}.txt", concentrado)
    guardar(f"extra_16digitos_{N}.txt", [rnd.randint(10**15, 10**16 - 1) for _ in range(N)])
    print("listo")


if __name__ == "__main__":
    main()
