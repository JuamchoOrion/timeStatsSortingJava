/**
 * Uso (desde la raíz del repo, tras compilar con: javac -d java/out java/*.java):
 *   java -cp java/out EjecutarComparativos <insertion|dualpivot|merge|heap> <aleatorio|asc|desc>
 * Se ejecuta una configuración por proceso para poder abortar un caso que pase de 5 minutos
 * (ver correr_java.sh, que recorre las 12 combinaciones).
 */
public class EjecutarComparativos {
    public static void main(String[] args) throws Exception {
        String a = args[0], v = args[1];
        switch (a) {
            case "insertion": Arnes.correr("Insertion Sort", Ordenamientos::insertionSort, v,
                    v.equals("asc") ? "n" : "n2"); break;
            case "dualpivot": Arnes.correr("Dual-Pivot QuickSort", Ordenamientos::dualPivotQuicksort, v,
                    v.equals("aleatorio") ? "nlogn" : "n2"); break;
            case "merge": Arnes.correr("Merge Sort", Ordenamientos::mergeSort, v, "nlogn"); break;
            case "heap": Arnes.correr("Heap Sort", Ordenamientos::heapSort, v, "nlogn"); break;
            default: throw new IllegalArgumentException("algoritmo desconocido: " + a);
        }
        // Si un hilo quedó trabajando tras un timeout, se mata el proceso (todo ya está escrito en el CSV).
        if (Arnes.huboTimeout) Runtime.getRuntime().halt(0);
    }
}
