import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Locale;
import java.util.function.Consumer;

/**
 * EXPERIMENTO ADICIONAL del Punto 3.1 (Rol 2), solo en Java. ¿Qué pasa con Radix y Bucket cuando no se
 * cumplen sus supuestos? Datos generados con python/generar_datos_extra.py (semilla propia, n = 100.000).
 *
 *  - Bucket Sort: datos uniformes (aleatorio_100000.txt) frente a datos concentrados.
 *  - Radix Sort: números de 8 dígitos (aleatorio_100000.txt) frente a números de 16 dígitos (long).
 *  - Merge Sort como referencia comparativa, que no depende de la distribución ni de los dígitos.
 *
 * Uso (desde la raíz del repo):  java -cp java/out ExperimentoExtra
 * Escribe resultados/experimento_extra.csv con el mismo esquema que los demás CSV.
 * 1 calentamiento + 5 repeticiones sobre copias nuevas; copia y verificación fuera del tiempo.
 */
public class ExperimentoExtra {

    static final Path CSV = Paths.get("resultados", "experimento_extra.csv");
    static final int N = 100_000;

    public static void main(String[] args) throws IOException {
        int[] uniforme = Arnes.leer("aleatorio_" + N + ".txt");
        int[] concentrado = Arnes.leer("extra_concentrado_" + N + ".txt");
        long[] dig16 = leerLong("extra_16digitos_" + N + ".txt");
        long[] dig8 = new long[uniforme.length];
        for (int i = 0; i < dig8.length; i++) dig8[i] = uniforme[i];

        Files.createDirectories(CSV.getParent());
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(CSV))) {
            out.println(Arnes.ENCABEZADO);
            out.println(medirInt("Bucket Sort", "uniforme", uniforme, NoComparativos::bucketSort));
            out.println(medirInt("Bucket Sort", "concentrado", concentrado, NoComparativos::bucketSort));
            out.println(medirInt("Merge Sort", "uniforme", uniforme, Ordenamientos::mergeSort));
            out.println(medirInt("Merge Sort", "concentrado", concentrado, Ordenamientos::mergeSort));
            out.println(medirLong("Radix Sort", "8_digitos", dig8));
            out.println(medirLong("Radix Sort", "16_digitos", dig16));
        }
    }

    static long[] leerLong(String nombre) throws IOException {
        List<String> lineas = Files.readAllLines(Arnes.DATOS.resolve(nombre));
        return lineas.stream().filter(s -> !s.isBlank()).mapToLong(s -> Long.parseLong(s.trim())).toArray();
    }

    static String medirInt(String alg, String variante, int[] original, Consumer<int[]> fn) {
        fn.accept(original.clone());                       // calentamiento (descartado)
        double[] t = new double[Arnes.REPS];
        for (int r = 0; r < t.length; r++) {
            int[] copia = original.clone();                // copia FUERA del tiempo
            long ini = System.nanoTime();
            fn.accept(copia);
            t[r] = System.nanoTime() - ini;
            for (int i = 1; i < copia.length; i++)         // verificación FUERA del tiempo
                if (copia[i - 1] > copia[i]) throw new IllegalStateException(alg + " no ordenó");
        }
        return fila(alg, variante, original.length, t);
    }

    // Radix con long en las dos variantes, para que la única diferencia sea el número de dígitos (8 vs 16 pasadas)
    static String medirLong(String alg, String variante, long[] original) {
        NoComparativos.radixSortLong(original.clone());
        double[] t = new double[Arnes.REPS];
        for (int r = 0; r < t.length; r++) {
            long[] copia = original.clone();
            long ini = System.nanoTime();
            NoComparativos.radixSortLong(copia);
            t[r] = System.nanoTime() - ini;
            for (int i = 1; i < copia.length; i++)
                if (copia[i - 1] > copia[i]) throw new IllegalStateException(alg + " no ordenó");
        }
        return fila(alg, variante, original.length, t);
    }

    static String fila(String alg, String variante, int n, double[] t) {
        double prom = 0;
        for (double v : t) prom += v;
        prom /= t.length;
        double s = 0;
        for (double v : t) s += (v - prom) * (v - prom);
        double desv = Math.sqrt(s / (t.length - 1));
        System.out.printf(Locale.ROOT, "[Java] %s %s n=%d: %.3f ms (+/-%.3f)%n", alg, variante, n, prom / 1e6, desv / 1e6);
        return String.format(Locale.ROOT, "%s,Java,%s,%d,%.0f,%.0f,%.0f,%.0f,%.0f,%.1f,%.1f,medido,experimento adicional",
                alg, variante, n, t[0], t[1], t[2], t[3], t[4], prom, desv);
    }
}
