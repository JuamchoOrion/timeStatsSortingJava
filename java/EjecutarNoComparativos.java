/**
 * Uso (desde la raíz del repo, tras compilar con: javac -d java/out java/*.java):
 *   java -cp java/out EjecutarNoComparativos <radix|bucket> <aleatorio|asc|desc>
 *   java -cp java/out EjecutarNoComparativos                (las 6 combinaciones)
 * Reutiliza el arnés del Rol 1 (Arnes.correr) y escribe resultados/ordenamiento_no_comparativos.csv
 * (un CSV por rol, mismo esquema).
 */
public class EjecutarNoComparativos {
    public static void main(String[] args) throws Exception {
        Arnes.CSV = java.nio.file.Paths.get("resultados", "ordenamiento_no_comparativos.csv");
        String[] algs = args.length > 0 ? new String[]{args[0]} : new String[]{"radix", "bucket"};
        String[] vars = args.length > 1 ? new String[]{args[1]} : new String[]{"aleatorio", "asc", "desc"};
        for (String a : algs) {
            for (String v : vars) {
                switch (a) {
                    // Ambos son O(n) con estos datos (d = 8 fijo; Bucket con datos uniformes): el modelo "n"
                    // solo se usa para estimar si un caso no terminara.
                    case "radix": Arnes.correr("Radix Sort", NoComparativos::radixSort, v, "n"); break;
                    case "bucket": Arnes.correr("Bucket Sort", NoComparativos::bucketSort, v, "n"); break;
                    default: throw new IllegalArgumentException("algoritmo desconocido: " + a);
                }
            }
        }
        if (Arnes.huboTimeout) Runtime.getRuntime().halt(0);
    }
}
