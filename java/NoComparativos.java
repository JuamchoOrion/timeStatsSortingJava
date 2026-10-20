import java.util.ArrayList;
import java.util.List;

/**
 * Algoritmos de ordenamiento NO basados en comparaciones (Rol 2). Ambos ordenan un int[].
 * Misma estructura que python/ordenamientos_no_comparativos.py (mismos nombres y mismo enfoque).
 *
 * Fuentes (GeeksforGeeks, completar con la fecha de consulta):
 *  - Radix Sort:  https://www.geeksforgeeks.org/radix-sort/
 *  - Bucket Sort: https://www.geeksforgeeks.org/bucket-sort-2/
 */
public class NoComparativos {

    // ------------------------------------------------------------ Radix Sort
    // LSD en base 10: una pasada de Counting Sort estable por dígito, del menos al más significativo.
    // Con números de 8 dígitos son 8 pasadas. Se eligió base 10 porque es la de GfG y la más fácil de
    // explicar; con base 256 serían 4 pasadas sobre bytes.
    public static void radixSort(int[] arr) {
        int n = arr.length;
        if (n == 0) return;
        int max = arr[0];
        for (int v : arr) if (v > max) max = v;
        int[] output = new int[n];
        for (int exp = 1; max / exp > 0; exp *= 10) countSort(arr, output, n, exp);
    }

    private static void countSort(int[] arr, int[] output, int n, int exp) {
        int[] count = new int[10];
        for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
        for (int i = 1; i < 10; i++) count[i] += count[i - 1];
        for (int i = n - 1; i >= 0; i--) {          // de atrás hacia adelante: mantiene la estabilidad
            int d = (arr[i] / exp) % 10;
            output[count[d] - 1] = arr[i];
            count[d]--;
        }
        System.arraycopy(output, 0, arr, 0, n);
    }

    // Misma lógica para long: solo se usa en el experimento adicional de 16 dígitos (Punto 3.1),
    // porque 16 dígitos no caben en int (máximo ≈ 2,1·10⁹).
    public static void radixSortLong(long[] arr) {
        int n = arr.length;
        if (n == 0) return;
        long max = arr[0];
        for (long v : arr) if (v > max) max = v;
        long[] output = new long[n];
        for (long exp = 1; max / exp > 0; exp *= 10) {
            int[] count = new int[10];
            for (int i = 0; i < n; i++) count[(int) ((arr[i] / exp) % 10)]++;
            for (int i = 1; i < 10; i++) count[i] += count[i - 1];
            for (int i = n - 1; i >= 0; i--) {
                int d = (int) ((arr[i] / exp) % 10);
                output[count[d] - 1] = arr[i];
                count[d]--;
            }
            System.arraycopy(output, 0, arr, 0, n);
            if (exp > Long.MAX_VALUE / 10) break;
        }
    }

    // ------------------------------------------------------------ Bucket Sort
    // k = n cubetas. El valor x va a la cubeta idx = (x - min) * k / (max - min + 1), calculado con
    // long para evitar desbordamiento. Así idx está siempre en [0, k-1]: el rango [min, max] se parte en
    // k intervalos de igual ancho. Cada cubeta se ordena con Insertion Sort (estable) y luego se concatenan.
    public static void bucketSort(int[] arr) {
        int n = arr.length;
        if (n == 0) return;
        int min = arr[0], max = arr[0];
        for (int v : arr) {
            if (v < min) min = v;
            if (v > max) max = v;
        }
        int k = n;
        long rango = (long) max - min + 1;
        List<List<Integer>> cubetas = new ArrayList<>(k);
        for (int i = 0; i < k; i++) cubetas.add(new ArrayList<>());
        for (int v : arr) {
            int idx = (int) (((long) v - min) * k / rango);
            cubetas.get(idx).add(v);
        }
        int pos = 0;
        for (List<Integer> c : cubetas) {
            insertionSortCubeta(c);
            for (int v : c) arr[pos++] = v;
        }
    }

    private static void insertionSortCubeta(List<Integer> c) {
        for (int i = 1; i < c.size(); i++) {
            int key = c.get(i);
            int j = i - 1;
            while (j >= 0 && c.get(j) > key) {
                c.set(j + 1, c.get(j));
                j--;
            }
            c.set(j + 1, key);
        }
    }
}
