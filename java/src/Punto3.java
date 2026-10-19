import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;
import java.util.Random;

/**
 * Experimento complementario del Punto 3.1: ¿qué pasa con Bucket Sort cuando no se cumple
 * su supuesto de distribución uniforme?
 *
 * Se comparan, con n = 100.000, los datos del taller (uniformes en [10^7, 10^8)) contra datos
 * concentrados: el 99 % de los valores cae en un rango de 1.000 números y el 1 % restante se
 * reparte en todo el rango de 8 dígitos (así min y max siguen siendo los mismos).
 *
 * Uso:  java -cp out Punto3 <raiz_repo>
 */
public class Punto3 {

    public static void main(String[] args) throws IOException {
        Path raiz = Paths.get(args.length > 0 ? args[0] : "..").toAbsolutePath().normalize();
        int n = 100_000;
        int[] uniforme = Experimentos.leer(raiz.resolve("datos/aleatorio_" + n + ".txt"));
        Random rnd = new Random(42);
        int[] concentrado = new int[n];
        for (int i = 0; i < n; i++) {
            concentrado[i] = rnd.nextInt(100) == 0
                    ? 10_000_000 + rnd.nextInt(90_000_000)
                    : 50_000_000 + rnd.nextInt(1_000);
        }
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(raiz.resolve("resultados/punto3_java.csv")))) {
            out.println(Experimentos.CABECERA);
            medir(out, "Bucket Sort", "uniforme", uniforme);
            medir(out, "Bucket Sort", "concentrado", concentrado);
            medir(out, "Dual-Pivot QuickSort", "uniforme", uniforme);
            medir(out, "Dual-Pivot QuickSort", "concentrado", concentrado);
        }
    }

    static void medir(PrintWriter out, String alg, String variante, int[] original) {
        java.util.function.Consumer<int[]> fn = alg.equals("Bucket Sort")
                ? Ordenamiento::bucketSort : Ordenamiento::dualPivotQuickSort;
        fn.accept(original.clone()); // calentamiento
        double[] t = new double[Experimentos.REPS];
        for (int r = 0; r < t.length; r++) {
            int[] copia = original.clone();
            System.gc();
            long t0 = System.nanoTime();
            fn.accept(copia);
            t[r] = System.nanoTime() - t0;
            if (!Ordenamiento.estaOrdenado(copia)) throw new IllegalStateException(alg);
        }
        out.println(Experimentos.filaMedida(alg, "punto3", variante, original.length, t, "verificado"));
        System.out.printf(Locale.ROOT, "%-22s %-12s %.3f ms%n", alg, variante, Experimentos.promedio(t) / 1e6);
    }
}
