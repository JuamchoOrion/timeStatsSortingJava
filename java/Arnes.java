import java.io.IOException;
import java.nio.file.*;
import java.util.Locale;
import java.util.StringTokenizer;

/**
 * Arnés de medición para ORDENAMIENTO (Rol 1). Rol 2 lo reutiliza con correr(...).
 * Ejecutar SIEMPRE desde la raíz del repo (usa rutas relativas datos/ y resultados/).
 *
 * - Calentamiento (1 ejecución, no entra en el promedio) + 5 repeticiones sobre copias nuevas.
 * - Copia y verificación FUERA del tiempo medido; cronometra solo el algoritmo (System.nanoTime()).
 * - Cada ejecución corre en un hilo con límite de 300 s; si lo excede o hay StackOverflowError,
 *   se escribe una fila ESTIMADA. Desviación estándar MUESTRAL (n-1).
 */
public class Arnes {
    public interface Ordenador { void ordenar(int[] a); }

    public static final int[] TAMANOS = {1000, 10000, 100000, 1000000};
    public static final int REPS = 5;
    public static final long LIMITE_MS = 300_000L;
    public static final Path DATOS = Paths.get("datos");
    public static final Path CSV = Paths.get("resultados", "ordenamiento_comparativos.csv");
    static final String ENCABEZADO =
        "algoritmo,lenguaje,variante,n,t1_ns,t2_ns,t3_ns,t4_ns,t5_ns,promedio_ns,desviacion_ns,tipo,observacion";

    /** true si alguna ejecución excedió el límite (el hilo sigue vivo: el main debe terminar con halt). */
    public static boolean huboTimeout = false;

    static class Fallo extends Exception {
        final String tipo;
        Fallo(String tipo, String msg) { super(msg); this.tipo = tipo; }
    }

    public static int[] leer(String nombre) throws IOException {
        String txt = new String(Files.readAllBytes(DATOS.resolve(nombre)));
        StringTokenizer st = new StringTokenizer(txt, " \t\r\n,;");
        int[] a = new int[st.countTokens()];
        for (int i = 0; st.hasMoreTokens(); i++) a[i] = Integer.parseInt(st.nextToken());
        return a;
    }

    static double factor(String modelo, double n) {
        if (modelo.equals("n2")) return n * n;
        if (modelo.equals("n")) return n;
        return n * (Math.log(n) / Math.log(2));
    }

    static String nombreModelo(String m) {
        return m.equals("n2") ? "O(n^2)" : m.equals("n") ? "O(n)" : "O(n log n)";
    }

    static long cronometrar(Ordenador alg, int[] original, long sumaOriginal) throws Fallo {
        final int[] copia = original.clone();              // copia FUERA del tiempo
        final long[] t = new long[1];
        final Throwable[] err = new Throwable[1];
        Thread th = new Thread(() -> {
            try {
                long ini = System.nanoTime();
                alg.ordenar(copia);
                t[0] = System.nanoTime() - ini;
            } catch (Throwable e) {
                err[0] = e;
            }
        });
        th.setDaemon(true);
        th.start();
        try {
            th.join(LIMITE_MS);
        } catch (InterruptedException e) {
            throw new Fallo("ERROR", "interrumpido");
        }
        if (th.isAlive()) {
            huboTimeout = true;
            throw new Fallo("TIMEOUT", "excedió " + (LIMITE_MS / 1000) + " s");
        }
        if (err[0] instanceof StackOverflowError) throw new Fallo("STACKOVERFLOW", "StackOverflowError");
        if (err[0] != null) throw new Fallo("ERROR", err[0].toString());
        long suma = 0;                                     // verificación FUERA del tiempo
        for (int i = 0; i < copia.length; i++) {
            if (i > 0 && copia[i - 1] > copia[i]) throw new Fallo("ERROR", "el arreglo no quedó ordenado");
            suma += copia[i];
        }
        if (suma != sumaOriginal) throw new Fallo("ERROR", "los elementos cambiaron");
        return t[0];
    }

    static synchronized void escribirFila(String fila) throws IOException {
        Files.createDirectories(CSV.getParent());
        boolean nuevo = !Files.exists(CSV) || Files.size(CSV) == 0;
        StringBuilder sb = new StringBuilder();
        if (nuevo) sb.append(ENCABEZADO).append('\n');
        sb.append(fila).append('\n');
        Files.write(CSV, sb.toString().getBytes(), StandardOpenOption.CREATE, StandardOpenOption.APPEND);
    }

    static String esc(String s) { return "\"" + s.replace("\"", "\"\"") + "\""; }

    /** modelo: "n2" | "n" | "nlogn" (solo se usa para estimar si el caso no termina o falla). */
    public static void correr(String nombre, Ordenador alg, String variante, String modelo) throws IOException {
        final String lenguaje = "Java";
        double t0 = -1;
        int n0 = -1;
        String causa = null;
        for (int n : TAMANOS) {
            if (causa != null) { estimado(nombre, lenguaje, variante, n, modelo, t0, n0, causa); continue; }
            int[] datos = leer(variante + "_" + n + ".txt");
            long suma = 0;
            for (int v : datos) suma += v;
            try {
                cronometrar(alg, datos, suma);                       // calentamiento (descartado)
                long[] ts = new long[REPS];
                for (int i = 0; i < REPS; i++) ts[i] = cronometrar(alg, datos, suma);
                double prom = 0;
                for (long x : ts) prom += x;
                prom /= REPS;
                double s = 0;
                for (long x : ts) s += (x - prom) * (x - prom);
                double desv = Math.sqrt(s / (REPS - 1));
                escribirFila(String.format(Locale.ROOT, "%s,%s,%s,%d,%d,%d,%d,%d,%d,%.1f,%.1f,medido,",
                    nombre, lenguaje, variante, n, ts[0], ts[1], ts[2], ts[3], ts[4], prom, desv));
                System.out.printf(Locale.ROOT, "[Java] %s %s n=%d: %.3f ms (±%.3f)%n",
                    nombre, variante, n, prom / 1e6, desv / 1e6);
                t0 = prom;
                n0 = n;
            } catch (Fallo e) {
                causa = e.tipo + ": " + e.getMessage() + " en n=" + n;
                System.out.println("[Java] " + nombre + " " + variante + " n=" + n + ": " + causa);
                estimado(nombre, lenguaje, variante, n, modelo, t0, n0, causa);
            }
        }
    }

    static void estimado(String nombre, String lenguaje, String variante, int n, String modelo,
                         double t0, int n0, String causa) throws IOException {
        String prom, obs;
        if (n0 < 0) {
            prom = "";
            obs = causa + "; sin medición previa para extrapolar";
        } else {
            prom = String.format(Locale.ROOT, "%.1f", t0 * factor(modelo, n) / factor(modelo, n0));
            obs = causa + "; extrapolado con " + nombreModelo(modelo) + " desde n=" + n0;
        }
        escribirFila(String.format(Locale.ROOT, "%s,%s,%s,%d,,,,,,%s,,estimado,%s",
            nombre, lenguaje, variante, n, prom, esc(obs)));
    }
}
