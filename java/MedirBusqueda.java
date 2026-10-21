import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

/**
 * Mediciones del Punto 2 (búsqueda) en Java.
 *
 * Uso (desde la raíz del repo):
 *   java MedirBusqueda.java                       -> tamaños 1.000, 10.000, 100.000, 1.000.000
 *   java MedirBusqueda.java . 1000,10000          -> solo esos tamaños (para pruebas)
 *
 * Escribe resultados/busqueda_java.csv con el esquema acordado:
 *   algoritmo,lenguaje,variante,n,t1_ns..t5_ns,promedio_ns,desviacion_ns,tipo,observacion
 * Cada t_i es el tiempo PROMEDIO POR BÚSQUEDA (ns) de la repetición i.
 *
 * Variantes:
 *   claves_mixtas  : las 1.000 claves de claves_n.txt sobre asc_n.txt
 *   pos_inicio / pos_centro / pos_final : 1.000 veces la misma clave (solo n = 1.000.000)
 *   claves_mixtas_desordenado : solo Lineal, n = 1.000.000, sobre aleatorio_n.txt (para el Punto 3.2)
 */
public class MedirBusqueda {

    static final int REPETICIONES = 5;
    static final int VECES_POSICION = 1000;
    static final String[] NOMBRES = {"Lineal", "Binaria", "Ternaria", "Saltos", "Interpolacion", "Exponencial"};
    /** Interfaz propia (en vez de ToIntBiFunction) para evitar boxing de la clave dentro del tiempo medido. */
    interface Buscador {
        int buscar(int[] a, int clave);
    }

    static final List<Buscador> ALGS = List.of(
            Busquedas::lineal, Busquedas::binaria, Busquedas::ternaria,
            Busquedas::saltos, Busquedas::interpolacion, Busquedas::exponencial);

    static volatile long sumidero;   // evita que el JIT elimine las búsquedas como código muerto

    public static void main(String[] args) throws IOException {
        Path raiz = Paths.get(args.length > 0 ? args[0] : ".");
        int[] tamanos = {1_000, 10_000, 100_000, 1_000_000};
        if (args.length > 1) {
            tamanos = Arrays.stream(args[1].split(",")).mapToInt(Integer::parseInt).toArray();
        }
        Files.createDirectories(raiz.resolve("resultados"));
        Path salida = raiz.resolve("resultados/busqueda_java.csv");

        try (PrintWriter csv = new PrintWriter(Files.newBufferedWriter(salida, StandardCharsets.UTF_8))) {
            csv.println("algoritmo,lenguaje,variante,n,t1_ns,t2_ns,t3_ns,t4_ns,t5_ns,promedio_ns,desviacion_ns,tipo,observacion");
            for (int n : tamanos) {
                int[] asc = leer(raiz.resolve("datos/asc_" + n + ".txt"));
                int[] claves = leer(raiz.resolve("datos/claves_" + n + ".txt"));
                System.out.println("n = " + n);

                for (int a = 0; a < ALGS.size(); a++) {
                    verificar(NOMBRES[a], ALGS.get(a), asc, claves);
                    medir(csv, NOMBRES[a], "claves_mixtas", n, ALGS.get(a), asc, claves);
                }
                if (n == 1_000_000) {
                    int[] pos = leer(raiz.resolve("datos/clave_pos_" + n + ".txt")); // inicio, centro, final
                    String[] variantes = {"pos_inicio", "pos_centro", "pos_final"};
                    for (int a = 0; a < ALGS.size(); a++) {
                        for (int p = 0; p < 3; p++) {
                            int[] repetida = new int[VECES_POSICION];
                            Arrays.fill(repetida, pos[p]);
                            medir(csv, NOMBRES[a], variantes[p], n, ALGS.get(a), asc, repetida);
                        }
                    }
                    // Lineal sobre el arreglo DESORDENADO (insumo del Punto 3.2).
                    int[] desordenado = leer(raiz.resolve("datos/aleatorio_" + n + ".txt"));
                    medir(csv, "Lineal", "claves_mixtas_desordenado", n, ALGS.get(0), desordenado, claves);
                }
            }
        }
        System.out.println("Listo: " + salida + "  (sumidero=" + sumidero + ")");
    }

    /** Verificación FUERA del tiempo medido: el resultado debe coincidir con Arrays.binarySearch. */
    static void verificar(String nombre, Buscador alg, int[] arr, int[] claves) {
        for (int clave : claves) {
            int r = alg.buscar(arr, clave);
            boolean presente = Arrays.binarySearch(arr, clave) >= 0;
            if (presente && (r < 0 || arr[r] != clave)) throw new IllegalStateException(nombre + " no encontró " + clave);
            if (!presente && r != -1) throw new IllegalStateException(nombre + " devolvió índice para clave ausente " + clave);
        }
    }

    static void medir(PrintWriter csv, String nombre, String variante, int n,
                      Buscador alg, int[] arr, int[] claves) {
        // Calentamiento (no se promedia): al menos 5 pasadas y 100 ms, para que el JIT compile el código.
        long acc = 0;
        long inicioCalentamiento = System.nanoTime();
        for (int pasada = 0; pasada < 5 || System.nanoTime() - inicioCalentamiento < 100_000_000L; pasada++) {
            for (int clave : claves) acc += alg.buscar(arr, clave);
            if (pasada > 2000) break;
        }
        sumidero += acc;

        double[] t = new double[REPETICIONES];
        for (int r = 0; r < REPETICIONES; r++) {
            long suma = 0;
            long t0 = System.nanoTime();
            for (int clave : claves) suma += alg.buscar(arr, clave);
            long t1 = System.nanoTime();
            sumidero += suma;
            t[r] = (double) (t1 - t0) / claves.length;      // ns por búsqueda
        }
        double prom = Arrays.stream(t).average().orElse(0);
        double var = Arrays.stream(t).map(x -> (x - prom) * (x - prom)).sum() / (REPETICIONES - 1);
        double desv = Math.sqrt(var);

        StringBuilder sb = new StringBuilder();
        sb.append(nombre).append(",java,").append(variante).append(',').append(n);
        for (double x : t) sb.append(',').append(String.format(Locale.ROOT, "%.3f", x));
        sb.append(',').append(String.format(Locale.ROOT, "%.3f,%.3f", prom, desv));
        sb.append(",medido,");
        csv.println(sb);
        csv.flush();
        System.out.printf(Locale.ROOT, "  %-14s %-26s %12.1f ns/búsqueda%n", nombre, variante, prom);
    }

    static int[] leer(Path p) throws IOException {
        List<Integer> v = new ArrayList<>();
        try (BufferedReader br = Files.newBufferedReader(p, StandardCharsets.UTF_8)) {
            String linea;
            while ((linea = br.readLine()) != null) {
                linea = linea.trim();
                if (!linea.isEmpty()) v.add(Integer.parseInt(linea));
            }
        }
        return v.stream().mapToInt(Integer::intValue).toArray();
    }
}
