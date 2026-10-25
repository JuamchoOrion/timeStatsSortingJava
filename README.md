Taller 3: ordenamiento y búsqueda (Java y Python)
Análisis de Algoritmos, Universidad del Quindío, octubre de 2026.

Integrantes: Laura Valentina Gomez Alzate, Maryam Hernández Giraldo y Juancho .

Comparamos seis algoritmos de ordenamiento (Insertion, Dual-Pivot QuickSort, Merge, Heap, Radix y Bucket) y seis de búsqueda (Lineal, Binaria, Ternaria, Saltos, Interpolación y Exponencial), implementados con la misma estructura en Java y en Python. Todas las corridas oficiales se hicieron en un Apple M2 con 16 GB, macOS 27.0.1, JDK 24.0.2 y Python 3.9.6.

Estructura
Carpeta	Contenido
java/	Implementaciones y programas de medición en Java
python/	Implementaciones, programas de medición, generadores de datos y ordenar_o_no.py (Punto 3.2)
python/graficas/	Módulo que lee los CSV y genera las gráficas y resultados/tablas.md
datos/	Arreglos de entrada (semilla 42) y datos del experimento adicional (semilla 2026)
resultados/	CSV con los tiempos de la corrida oficial y tablas.md
graficas/	Las 9 gráficas del informe en PNG
Cómo reproducir
Todo se ejecuta desde la raíz del repositorio.

# 1. Datos (ya están en datos/; esto los regenera igual)
python python/generar_datos.py
python python/generar_datos_extra.py

# 2. Java
javac -d java/out java/*.java
bash correr_java.sh                                  # comparativos, 4 algoritmos x 3 variantes
java -cp java/out EjecutarNoComparativos             # Radix y Bucket
java -cp java/out MedirBusqueda                      # búsquedas
java -cp java/out ExperimentoExtra                   # experimento adicional del Punto 3.1

# 3. Python
python python/ejecutar_comparativos.py
python python/ejecutar_no_comparativos.py
python python/medir_busqueda.py

# 4. Punto 3.2, gráficas y tablas
python python/ordenar_o_no.py
python -m pip install matplotlib
python python/graficas
Protocolo
Cada configuración se mide 5 veces y se reporta el promedio y la desviación estándar muestral. Los datos se cargan antes de iniciar el reloj (System.nanoTime() en Java, time.perf_counter_ns() en Python), cada repetición de ordenamiento usa una copia nueva del arreglo y el resultado se verifica fuera del tiempo. En Java se hace una ejecución de calentamiento que no se cuenta. Si una ejecución supera 5 minutos o falla por recursión, se registra en la columna observacion del CSV y el tiempo se estima con la complejidad teórica.

Fuentes
Las implementaciones siguen GeeksforGeeks; la URL de cada algoritmo está en un comentario sobre su función.