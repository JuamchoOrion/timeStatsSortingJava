# Tablas generadas a partir de resultados/*.csv

Promedio ± desviación estándar muestral de 5 repeticiones. *(est.)* = estimado.

## Ordenamiento – Java – entrada aleatoria

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Insertion Sort | 562.3 µs ± 192.5 µs | 4.40 ms ± 159.7 µs | 436.66 ms ± 3.37 ms | 44.58 s ± 53.19 ms |
| Dual-Pivot QuickSort | 54.7 µs ± 19.0 µs | 425.5 µs ± 9.8 µs | 5.06 ms ± 70.2 µs | 59.18 ms ± 305.7 µs |
| Merge Sort | 70.8 µs ± 7.6 µs | 1.28 ms ± 1.52 ms | 7.55 ms ± 71.3 µs | 91.38 ms ± 2.57 ms |
| Heap Sort | 123.0 µs ± 4.2 µs | 891.3 µs ± 145.7 µs | 8.56 ms ± 190.4 µs | 103.03 ms ± 1.15 ms |
| Radix Sort | 209.7 µs ± 118.1 µs | 583.8 µs ± 95.7 µs | 3.17 ms ± 91.1 µs | 28.15 ms ± 419.2 µs |
| Bucket Sort | 299.0 µs ± 9.0 µs | 879.2 µs ± 57.7 µs | 6.91 ms ± 1.67 ms | 128.00 ms ± 12.98 ms |

## Ordenamiento – Java – entrada ascendente

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Insertion Sort | 25.4 µs ± 3.3 µs | 239.0 µs ± 4.7 µs | 295.4 µs ± 29.1 µs | 219.6 µs ± 56.4 µs |
| Dual-Pivot QuickSort | 550.1 µs ± 404.1 µs | 8.58 ms ± 41.4 µs | *857.86 ms (est.)* | *1.4 min (est.)* |
| Merge Sort | 38.1 µs ± 3.2 µs | 611.7 µs ± 970.1 µs | 2.05 ms ± 117.0 µs | 22.51 ms ± 224.0 µs |
| Heap Sort | 114.8 µs ± 6.3 µs | 684.6 µs ± 162.0 µs | 5.49 ms ± 183.7 µs | 57.35 ms ± 840.0 µs |
| Radix Sort | 32.8 µs ± 825 ns | 318.1 µs ± 15.2 µs | 2.88 ms ± 29.2 µs | 28.15 ms ± 191.4 µs |
| Bucket Sort | 29.2 µs ± 5.8 µs | 332.6 µs ± 9.2 µs | 6.32 ms ± 4.45 ms | 48.69 ms ± 14.27 ms |

## Ordenamiento – Java – entrada descendente

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Insertion Sort | 629.2 µs ± 361.1 µs | 13.11 ms ± 9.88 ms | 887.80 ms ± 5.83 ms | 1.5 min ± 1.36 s |
| Dual-Pivot QuickSort | 651.6 µs ± 314.6 µs | 8.51 ms ± 76.9 µs | *851.30 ms (est.)* | *1.4 min (est.)* |
| Merge Sort | 41.0 µs ± 3.7 µs | 1.13 ms ± 1.54 ms | 2.93 ms ± 992.1 µs | 23.41 ms ± 239.7 µs |
| Heap Sort | 108.3 µs ± 3.4 µs | 667.9 µs ± 128.2 µs | 5.67 ms ± 166.1 µs | 60.02 ms ± 439.5 µs |
| Radix Sort | 38.2 µs ± 2.6 µs | 300.5 µs ± 1.9 µs | 2.79 ms ± 26.9 µs | 27.88 ms ± 234.6 µs |
| Bucket Sort | 38.4 µs ± 3.7 µs | 351.8 µs ± 14.8 µs | 3.32 ms ± 58.3 µs | 55.13 ms ± 16.70 ms |

## Ordenamiento – Python – entrada aleatoria

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Insertion Sort | 20.23 ms ± 1.36 ms | 2.09 s ± 16.31 ms | 3.5 min ± 1.29 s | *5.8 h (est.)* |
| Dual-Pivot QuickSort | 830.4 µs ± 16.9 µs | 10.53 ms ± 14.4 µs | 140.00 ms ± 505.2 µs | 1.64 s ± 4.06 ms |
| Merge Sort | 1.45 ms ± 26.8 µs | 18.64 ms ± 161.2 µs | 224.77 ms ± 646.9 µs | 2.70 s ± 6.79 ms |
| Heap Sort | 1.83 ms ± 15.7 µs | 25.53 ms ± 294.1 µs | 324.64 ms ± 3.99 ms | 4.17 s ± 10.55 ms |
| Radix Sort | 1.88 ms ± 36.5 µs | 16.25 ms ± 921.2 µs | 157.57 ms ± 563.4 µs | 2.33 s ± 30.87 ms |
| Bucket Sort | 444.5 µs ± 46.2 µs | 4.28 ms ± 205.6 µs | 46.72 ms ± 2.74 ms | 741.77 ms ± 14.40 ms |

## Ordenamiento – Python – entrada ascendente

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Insertion Sort | 91.5 µs ± 735 ns | 949.5 µs ± 11.6 µs | 9.53 ms ± 64.3 µs | 95.23 ms ± 246.0 µs |
| Dual-Pivot QuickSort | 17.59 ms ± 86.7 µs | *1.76 s (est.)* | *2.9 min (est.)* | *4.9 h (est.)* |
| Merge Sort | 1.23 ms ± 6.0 µs | 15.65 ms ± 10.5 µs | 186.12 ms ± 349.1 µs | 2.15 s ± 1.53 ms |
| Heap Sort | 1.93 ms ± 11.3 µs | 26.44 ms ± 19.4 µs | 333.43 ms ± 686.6 µs | 4.01 s ± 4.26 ms |
| Radix Sort | 1.56 ms ± 73.1 µs | 15.85 ms ± 131.3 µs | 157.93 ms ± 696.9 µs | 1.92 s ± 4.29 ms |
| Bucket Sort | 412.3 µs ± 7.5 µs | 4.13 ms ± 195.5 µs | 43.90 ms ± 643.7 µs | 505.61 ms ± 7.70 ms |

## Ordenamiento – Python – entrada descendente

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Insertion Sort | 39.91 ms ± 447.6 µs | 4.13 s ± 3.74 ms | *6.9 min (est.)* | *11.5 h (est.)* |
| Dual-Pivot QuickSort | 17.69 ms ± 151.2 µs | *1.77 s (est.)* | *2.9 min (est.)* | *4.9 h (est.)* |
| Merge Sort | 1.24 ms ± 8.8 µs | 15.56 ms ± 12.2 µs | 186.20 ms ± 982.3 µs | 2.15 s ± 1.41 ms |
| Heap Sort | 1.68 ms ± 19.9 µs | 23.97 ms ± 194.3 µs | 306.74 ms ± 921.2 µs | 3.77 s ± 3.85 ms |
| Radix Sort | 1.57 ms ± 87.5 µs | 15.72 ms ± 180.8 µs | 157.37 ms ± 861.3 µs | 1.89 s ± 7.82 ms |
| Bucket Sort | 429.9 µs ± 11.5 µs | 4.38 ms ± 157.7 µs | 45.53 ms ± 972.5 µs | 536.99 ms ± 10.28 ms |

## Factor de crecimiento T(10n)/T(n), entrada aleatoria

Entre paréntesis, la razón que predice la complejidad teórica. *(est.)* = usa un valor estimado.

| Algoritmo | Lenguaje | 1k→10k | 10k→100k | 100k→1M |
|---|---|---|---|---|
| Insertion Sort | Java | 7.8 (100.0) | 99.3 (100.0) | 102.1 (100.0) |
| Dual-Pivot QuickSort | Java | 7.8 (13.3) | 11.9 (12.5) | 11.7 (12.0) |
| Merge Sort | Java | 18.1 (13.3) | 5.9 (12.5) | 12.1 (12.0) |
| Heap Sort | Java | 7.2 (13.3) | 9.6 (12.5) | 12.0 (12.0) |
| Radix Sort | Java | 2.8 (10.0) | 5.4 (10.0) | 8.9 (10.0) |
| Bucket Sort | Java | 2.9 (10.0) | 7.9 (10.0) | 18.5 (10.0) |
| Insertion Sort | Python | 103.3 (100.0) | 99.6 (100.0) | 100.0 (est.) (100.0) |
| Dual-Pivot QuickSort | Python | 12.7 (13.3) | 13.3 (12.5) | 11.7 (12.0) |
| Merge Sort | Python | 12.8 (13.3) | 12.1 (12.5) | 12.0 (12.0) |
| Heap Sort | Python | 14.0 (13.3) | 12.7 (12.5) | 12.8 (12.0) |
| Radix Sort | Python | 8.6 (10.0) | 9.7 (10.0) | 14.8 (10.0) |
| Bucket Sort | Python | 9.6 (10.0) | 10.9 (10.0) | 15.9 (10.0) |

## Compilado vs interpretado – ordenamiento, n = 1.000.000, entrada aleatoria

| Algoritmo | Java | Python | Python / Java |
|---|---|---|---|
| Insertion Sort | 44.58 s ± 53.19 ms | *5.8 h (est.)* | 466.9 |
| Dual-Pivot QuickSort | 59.18 ms ± 305.7 µs | 1.64 s ± 4.06 ms | 27.8 |
| Merge Sort | 91.38 ms ± 2.57 ms | 2.70 s ± 6.79 ms | 29.5 |
| Heap Sort | 103.03 ms ± 1.15 ms | 4.17 s ± 10.55 ms | 40.5 |
| Radix Sort | 28.15 ms ± 419.2 µs | 2.33 s ± 30.87 ms | 82.8 |
| Bucket Sort | 128.00 ms ± 12.98 ms | 741.77 ms ± 14.40 ms | 5.8 |

## Búsqueda – Java – tiempo promedio por búsqueda (1.000 claves mixtas)

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Lineal | 132 ns ± 6 ns | 1.3 µs ± 38 ns | 13.2 µs ± 197 ns | 128.6 µs ± 1.6 µs |
| Binaria | 70 ns ± 6 ns | 55 ns ± 10 ns | 80 ns ± 7 ns | 103 ns ± 15 ns |
| Ternaria | 50 ns ± 24 ns | 51 ns ± 8 ns | 106 ns ± 16 ns | 94 ns ± 4 ns |
| Saltos | 58 ns ± 24 ns | 93 ns ± 9 ns | 235 ns ± 0 ns | 688 ns ± 6 ns |
| Interpolacion | 33 ns ± 21 ns | 22 ns ± 11 ns | 49 ns ± 7 ns | 30 ns ± 14 ns |
| Exponencial | 45 ns ± 6 ns | 66 ns ± 10 ns | 87 ns ± 18 ns | 98 ns ± 2 ns |

## Búsqueda – Python – tiempo promedio por búsqueda (1.000 claves mixtas)

| Algoritmo | n=1.000 | n=10.000 | n=100.000 | n=1.000.000 |
|---|---|---|---|---|
| Lineal | 20.0 µs ± 695 ns | 211.2 µs ± 1.3 µs | 2.26 ms ± 56.8 µs | 21.53 ms ± 349.8 µs |
| Binaria | 1.2 µs ± 97 ns | 1.7 µs ± 73 ns | 2.2 µs ± 79 ns | 2.5 µs ± 117 ns |
| Ternaria | 1.2 µs ± 58 ns | 1.5 µs ± 87 ns | 2.1 µs ± 82 ns | 2.4 µs ± 154 ns |
| Saltos | 3.2 µs ± 125 ns | 9.4 µs ± 133 ns | 29.8 µs ± 363 ns | 91.5 µs ± 431 ns |
| Interpolacion | 905 ns ± 67 ns | 1.1 µs ± 71 ns | 1.2 µs ± 32 ns | 1.2 µs ± 131 ns |
| Exponencial | 1.6 µs ± 71 ns | 2.1 µs ± 109 ns | 2.7 µs ± 58 ns | 3.4 µs ± 199 ns |

## Posición de la clave – Java – n = 1.000.000 (tiempo promedio por búsqueda)

| Algoritmo | Inicio | Centro | Final |
|---|---|---|---|
| Lineal | 3 ns ± 0 ns | 83.3 µs ± 797 ns | 164.6 µs ± 923 ns |
| Binaria | 24 ns ± 1 ns | 24 ns ± 0 ns | 28 ns ± 3 ns |
| Ternaria | 32 ns ± 1 ns | 30 ns ± 1 ns | 32 ns ± 0 ns |
| Saltos | 4 ns ± 0 ns | 496 ns ± 1 ns | 1.3 µs ± 26 ns |
| Interpolacion | 4 ns ± 0 ns | 7 ns ± 0 ns | 5 ns ± 4 ns |
| Exponencial | 3 ns ± 0 ns | 30 ns ± 0 ns | 38 ns ± 0 ns |

## Posición de la clave – Python – n = 1.000.000 (tiempo promedio por búsqueda)

| Algoritmo | Inicio | Centro | Final |
|---|---|---|---|
| Lineal | 200 ns ± 1 ns | 14.08 ms ± 90.0 µs | 28.20 ms ± 26.9 µs |
| Binaria | 2.2 µs ± 76 ns | 2.3 µs ± 102 ns | 2.4 µs ± 46 ns |
| Ternaria | 2.0 µs ± 93 ns | 2.3 µs ± 75 ns | 2.3 µs ± 122 ns |
| Saltos | 529 ns ± 27 ns | 65.6 µs ± 526 ns | 179.1 µs ± 842 ns |
| Interpolacion | 303 ns ± 22 ns | 892 ns ± 54 ns | 317 ns ± 1 ns |
| Exponencial | 110 ns ± 2 ns | 2.8 µs ± 91 ns | 3.5 µs ± 174 ns |

