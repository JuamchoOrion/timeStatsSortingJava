import random
from pathlib import Path

SEMILLA = 42
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
MIN_VAL, MAX_VAL = 10_000_000, 99_999_999   # 8 dígitos
NUM_CLAVES = 1_000                           # 500 presentes + 500 ausentes
DATOS = Path(__file__).resolve().parent.parent / "datos"


def guardar(nombre, valores):
    with open(DATOS / nombre, "w") as f:
        f.write("\n".join(map(str, valores)) + "\n")


def main():
    DATOS.mkdir(exist_ok=True)
    rnd = random.Random(SEMILLA)

    for n in TAMANOS:
        arr = [rnd.randint(MIN_VAL, MAX_VAL) for _ in range(n)]
        asc = sorted(arr)
        desc = asc[::-1]

        guardar(f"aleatorio_{n}.txt", arr)
        guardar(f"asc_{n}.txt", asc)
        guardar(f"desc_{n}.txt", desc)

        # Claves de búsqueda: 500 presentes y 500 ausentes
        presentes = rnd.sample(arr, NUM_CLAVES // 2)
        existentes = set(arr)
        ausentes = []
        while len(ausentes) < NUM_CLAVES // 2:
            c = rnd.randint(MIN_VAL, MAX_VAL)
            if c not in existentes:
                ausentes.append(c)
        claves = presentes + ausentes
        rnd.shuffle(claves)
        guardar(f"claves_{n}.txt", claves)

        # Claves por posición (inicio, centro, final) tomadas del arreglo ordenado
        guardar(f"clave_pos_{n}.txt", [asc[0], asc[n // 2], asc[-1]])

        print(f"n={n}: listo")


if __name__ == "__main__":
    main()
