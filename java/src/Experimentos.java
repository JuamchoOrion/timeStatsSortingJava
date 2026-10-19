import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.function.Consumer;
import java.util.function.ToIntBiFunction;

/**
 * Medición de tiempos del taller (lenguaje compilado: Java).
 *
 * Uso:  java -cp out Experimentos <raiz_repo> [ordenamiento|busqueda|todo] [n1,n2,...]
 *
 * Reglas aplicadas (enunciado del taller):
 *  - Los datos se leen de datos/*.txt antes de medir; la lectura no entra en el tiempo.
 *  - System.nanoTime(), 5 repeticiones, promedio y desviación estándar (muestral).
 *  - 1 ejecución de calentamiento (JIT) antes de las 5 repeticiones, no se promedia.
 *  - Ordenamiento: cada repetición trabaja sobre una copia nueva; la copia no se mide.
 *    Después de cada repetición (fuera del tiempo) se verifica que quedó ordenado.
 *  - Antes de cada repetición se llama a System.gc() (fuera del tiempo) para que la basura
 *    de la repetición anterior no se recolecte en medio de la medición.
 *  - Si el tiempo previsto de UNA ejecución supera 5 minutos, no se ejecuta: se estima
 *    a partir del tamaño anterior y de la complejidad teórica, y se marca "estimado".
 *  - Si la ejecución falla (StackOverflowError), se documenta y se estima.
 */
public class Experimentos {

    static final int REPS = 5;
    static final double LIMITE_NS = 300e9; // 5 minutos
    static final int[] TAMANOS = {1_000, 10_000, 100_000, 1_000_000};
    static final String[] VARIANTES = {"aleatorio", "asc", "desc"};
    static final String LENGUAJE = "Java";
    static long sumidero = 0; // evita que el JIT elimine las búsquedas como código muerto

    record Algoritmo(String nombre, Consumer<int[]> fn) {}
    record Buscador(String nombre, ToIntBiFunction<int[], Integer> fn) {}
    record Medido(int n, double promedio) {}

    static final List<Algoritmo> ORDENAMIENTOS = List.of(
            new Algoritmo("Insertion Sort", Ordenamiento::insertionSort),
            new Algoritmo("Dual-Pivot QuickSort", Ordenamiento::dualPivotQuickSort),
            new Algoritmo("Merge Sort", Ordenamiento::mergeSort),
            new Algoritmo("Heap Sort", Ordenamiento::heapSort),
            new Algoritmo("Radix Sort", Ordenamiento::radixSort),
            new Algoritmo("Bucket Sort", Ordenamiento::bucketSort));

    static final List<Buscador> BUSQUEDAS = List.of(
            new Buscador("Lineal", Busqueda::lineal),
            new Buscador("Binaria", Busqueda::binaria),
            new Buscador("Ternaria", Busqueda::ternaria),
            new Buscador("Saltos", Busqueda::saltos),
            new Buscador("Interpolacion", Busqueda::interpolacion),
            new Buscador("Exponencial", Busqueda::exponencial));

    /** Complejidad que se usa para estimar: "n", "nlogn" o "n2". */
    static String modelo(String alg, String variante) {
        switch (alg) {
            case "Insertion Sort":
                return variante.equals("asc") ? "n" : "n2";
            case "Dual-Pivot QuickSort":
                return variante.equals("aleatorio") ? "nlogn" : "n2";
            case "Radix Sort":
            case "Bucket Sort":
                return "n";
            default:
                return "nlogn";
        }
    }

    static double g(String modelo, double n) {
        switch (modelo) {
            case "n": return n;
            case "n2": return n * n;
            default: return n * Math.log(n) / Math.log(2);
        }
    }

    // ----------------------------------------------------------------- utilidades

    static int[] leer(Path p) throws IOException {
        List<String> lineas = Files.readAllLines(p);
        int[] a = new int[lineas.size()];
        for (int i = 0; i < a.length; i++) a[i] = Integer.parseInt(lineas.get(i).trim());
        return a;
    }

    static double promedio(double[] t) {
        double s = 0;
        for (double v : t) s += v;
        return s / t.length;
    }

    static double desviacion(double[] t) {
        double m = promedio(t), s = 0;
        for (double v : t) s += (v - m) * (v - m);
        return Math.sqrt(s / (t.length - 1));
    }

    static final String CABECERA =
            "algoritmo,lenguaje,punto,variante,n,t1_ns,t2_ns,t3_ns,t4_ns,t5_ns,promedio_ns,desv_ns,tipo,nota";

    static String filaMedida(String alg, String punto, String variante, int n, double[] t, String nota) {
        StringBuilder sb = new StringBuilder();
        sb.append(alg).append(',').append(LENGUAJE).append(',').append(punto).append(',')
                .append(variante).append(',').append(n);
        for (double v : t) sb.append(',').append(String.format(Locale.ROOT, "%.1f", v));
        sb.append(',').append(String.format(Locale.ROOT, "%.1f", promedio(t)))
                .append(',').append(String.format(Locale.ROOT, "%.1f", desviacion(t)))
                .append(",medido,").append(nota);
        return sb.toString();
    }

    static String filaEstimada(String alg, String punto, String variante, int n, double est, String nota) {
        return String.format(Locale.ROOT, "%s,%s,%s,%s,%d,,,,,,%.1f,,estimado,%s",
                alg, LENGUAJE, punto, variante, n, est, nota);
    }

    // ----------------------------------------------------------------- Punto 1

    static void ordenamiento(Path raiz, int[] tamanos) throws IOException {
        Path salida = raiz.resolve("resultados/ordenamiento_java.csv");
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(salida))) {
            out.println(CABECERA);
            Map<String, Medido> ultimo = new HashMap<>();
            Map<String, String> fallo = new HashMap<>();
            for (int n : tamanos) {
                for (String variante : VARIANTES) {
                    int[] original = leer(raiz.resolve("datos/" + variante + "_" + n + ".txt"));
                    for (Algoritmo a : ORDENAMIENTOS) {
                        String clave = a.nombre() + "|" + variante;
                        String mod = modelo(a.nombre(), variante);
                        Medido prev = ultimo.get(clave);
                        double previsto = prev == null ? 0 : prev.promedio() * g(mod, n) / g(mod, prev.n());

                        if (fallo.containsKey(clave) || previsto > LIMITE_NS) {
                            String motivo = fallo.containsKey(clave)
                                    ? fallo.get(clave)
                                    : String.format(Locale.ROOT, "previsto %.0f s > 5 min", previsto / 1e9);
                            String nota = String.format("no ejecutado (%s); estimado desde n=%d con modelo %s",
                                    motivo, prev.n(), mod);
                            out.println(filaEstimada(a.nombre(), "ordenamiento", variante, n, previsto, nota));
                            System.out.printf("%-22s %-9s n=%-8d ESTIMADO %.3f s%n", a.nombre(), variante, n, previsto / 1e9);
                            out.flush();
                            continue;
                        }

                        double[] t = new double[REPS];
                        try {
                            a.fn().accept(original.clone()); // calentamiento JIT
                            for (int r = 0; r < REPS; r++) {
                                int[] copia = original.clone();
                                System.gc(); // limpia la basura de la repetición anterior (fuera del tiempo)
                                long t0 = System.nanoTime();
                                a.fn().accept(copia);
                                long t1 = System.nanoTime();
                                t[r] = t1 - t0;
                                if (!Ordenamiento.estaOrdenado(copia))
                                    throw new IllegalStateException(a.nombre() + " no ordenó correctamente");
                            }
                        } catch (StackOverflowError e) {
                            String motivo = "StackOverflowError: la recursión superó la pila de la JVM";
                            fallo.put(clave, motivo);
                            if (prev == null) {
                                out.printf("%s,%s,ordenamiento,%s,%d,,,,,,,,error,%s%n", a.nombre(), LENGUAJE, variante, n, motivo);
                            } else {
                                String nota = String.format("%s; estimado desde n=%d con modelo %s", motivo, prev.n(), mod);
                                out.println(filaEstimada(a.nombre(), "ordenamiento", variante, n, previsto, nota));
                            }
                            System.out.printf("%-22s %-9s n=%-8d FALLO (%s)%n", a.nombre(), variante, n, motivo);
                            out.flush();
                            continue;
                        }
                        out.println(filaMedida(a.nombre(), "ordenamiento", variante, n, t, "verificado"));
                        out.flush();
                        ultimo.put(clave, new Medido(n, promedio(t)));
                        System.out.printf("%-22s %-9s n=%-8d %.6f s (desv %.6f)%n",
                                a.nombre(), variante, n, promedio(t) / 1e9, desviacion(t) / 1e9);
                    }
                }
            }
        }
    }

    // ----------------------------------------------------------------- Punto 2

    static void busqueda(Path raiz, int[] tamanos) throws IOException {
        Path salida = raiz.resolve("resultados/busqueda_java.csv");
        String[] nombresPos = {"inicio", "centro", "final"};
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(salida))) {
            out.println(CABECERA);
            for (int n : tamanos) {
                int[] arr = leer(raiz.resolve("datos/asc_" + n + ".txt"));
                int[] claves = leer(raiz.resolve("datos/claves_" + n + ".txt"));
                int[] pos = leer(raiz.resolve("datos/clave_pos_" + n + ".txt"));
                for (Buscador b : BUSQUEDAS) {
                    verificar(b, arr, claves);
                    // 1) las 1.000 claves (500 presentes + 500 ausentes)
                    double[] t = medirBusquedas(b, arr, claves);
                    out.println(filaMedida(b.nombre(), "busqueda", "claves", n, t,
                            "tiempo promedio por busqueda (total de 1000 / 1000)"));
                    System.out.printf("%-14s claves  n=%-8d %.1f ns/busqueda%n", b.nombre(), n, promedio(t));
                    // 2) misma clave 1.000 veces: inicio, centro y final
                    for (int p = 0; p < 3; p++) {
                        int[] repetida = new int[1000];
                        java.util.Arrays.fill(repetida, pos[p]);
                        double[] tp = medirBusquedas(b, arr, repetida);
                        out.println(filaMedida(b.nombre(), "busqueda", nombresPos[p], n, tp,
                                "tiempo promedio por busqueda (1000 veces la misma clave)"));
                    }
                    out.flush();
                }
            }
        }
        System.out.println("sumidero=" + sumidero);
    }

    /** Devuelve, por repetición, el tiempo promedio por búsqueda en ns. */
    static double[] medirBusquedas(Buscador b, int[] arr, int[] claves) {
        for (int c : claves) sumidero += b.fn().applyAsInt(arr, c); // calentamiento JIT
        double[] t = new double[REPS];
        for (int r = 0; r < REPS; r++) {
            System.gc();
            long acc = 0;
            long t0 = System.nanoTime();
            for (int c : claves) acc += b.fn().applyAsInt(arr, c);
            long t1 = System.nanoTime();
            sumidero += acc;
            t[r] = (double) (t1 - t0) / claves.length;
        }
        return t;
    }

    /** Fuera del tiempo medido: cada resultado debe coincidir con la búsqueda lineal. */
    static void verificar(Buscador b, int[] arr, int[] claves) {
        for (int c : claves) {
            int i = b.fn().applyAsInt(arr, c);
            boolean existe = Busqueda.lineal(arr, c) != -1;
            if (existe ? (i < 0 || arr[i] != c) : i != -1)
                throw new IllegalStateException(b.nombre() + " falló con la clave " + c);
        }
    }

    /**
     * Calentamiento global antes de cualquier medición: el JIT de la JVM necesita miles de
     * invocaciones para compilar un método con optimizaciones (C2). Con una sola ejecución de
     * calentamiento, los tamaños pequeños quedarían midiendo código interpretado.
     * Nada de esto se registra.
     */
    static void calentamientoGlobal(Path raiz) throws IOException {
        int[] base = leer(raiz.resolve("datos/aleatorio_10000.txt"));
        int[] asc = leer(raiz.resolve("datos/asc_10000.txt"));
        for (Algoritmo a : ORDENAMIENTOS) {
            int veces = a.nombre().equals("Insertion Sort") ? 10 : 50;
            for (int i = 0; i < veces; i++) a.fn().accept(base.clone());
        }
        for (Buscador b : BUSQUEDAS)
            for (int i = 0; i < 50_000; i++) sumidero += b.fn().applyAsInt(asc, base[i % base.length]);
    }

    public static void main(String[] args) throws IOException {
        Path raiz = Paths.get(args.length > 0 ? args[0] : "..").toAbsolutePath().normalize();
        String modo = args.length > 1 ? args[1] : "todo";
        int[] tamanos = TAMANOS;
        if (args.length > 2) {
            String[] partes = args[2].split(",");
            tamanos = new int[partes.length];
            for (int i = 0; i < partes.length; i++) tamanos[i] = Integer.parseInt(partes[i]);
        }
        Files.createDirectories(raiz.resolve("resultados"));
        calentamientoGlobal(raiz);
        if (modo.equals("ordenamiento") || modo.equals("todo")) ordenamiento(raiz, tamanos);
        if (modo.equals("busqueda") || modo.equals("todo")) busqueda(raiz, tamanos);
    }
}
