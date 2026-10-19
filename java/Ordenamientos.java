/**
 * Algoritmos de ordenamiento por comparación (Rol 1). Todos ordenan IN SITU un int[].
 * Misma estructura que python/ordenamientos_comparativos.py.
 *
 * Fuentes (GeeksforGeeks, completar con la fecha de consulta):
 *  - Insertion Sort:       https://www.geeksforgeeks.org/insertion-sort-algorithm/
 *  - Dual-Pivot QuickSort: https://www.geeksforgeeks.org/dual-pivot-quicksort/
 *  - Merge Sort:           https://www.geeksforgeeks.org/merge-sort/
 *  - Heap Sort:            https://www.geeksforgeeks.org/heap-sort/
 */
public class Ordenamientos {

    // ------------------------------------------------------------ Insertion Sort
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int k = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > k) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = k;
        }
    }

    // ------------------------------------------------------------ Dual-Pivot QuickSort
    public static void dualPivotQuicksort(int[] arr) {
        dpq(arr, 0, arr.length - 1);
    }

    // Recursivo, SIN cambiar el tamaño de pila (-Xss): si falla, se documenta.
    private static void dpq(int[] arr, int low, int high) {
        if (low < high) {
            int[] p = particion(arr, low, high);
            dpq(arr, low, p[0] - 1);
            dpq(arr, p[0] + 1, p[1] - 1);
            dpq(arr, p[1] + 1, high);
        }
    }

    private static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }

    private static int[] particion(int[] arr, int low, int high) {
        if (arr[low] > arr[high]) swap(arr, low, high);   // pivotes: primero y último (p <= q)
        int j = low + 1, g = high - 1, k = low + 1;
        int p = arr[low], q = arr[high];
        while (k <= g) {
            if (arr[k] < p) {
                swap(arr, k, j);
                j++;
            } else if (arr[k] >= q) {
                while (arr[g] > q && k < g) g--;
                swap(arr, k, g);
                g--;
                if (arr[k] < p) {
                    swap(arr, k, j);
                    j++;
                }
            }
            k++;
        }
        j--;
        g++;
        swap(arr, low, j);
        swap(arr, high, g);
        return new int[]{j, g};
    }

    // ------------------------------------------------------------ Merge Sort
    public static void mergeSort(int[] arr) {
        if (arr.length < 2) return;
        int[] aux = arr.clone();                 // auxiliar asignado UNA sola vez
        ms(arr, aux, 0, arr.length - 1);
    }

    private static void ms(int[] arr, int[] aux, int lo, int hi) {
        if (lo >= hi) return;
        int mid = (lo + hi) >>> 1;
        ms(arr, aux, lo, mid);
        ms(arr, aux, mid + 1, hi);
        System.arraycopy(arr, lo, aux, lo, hi - lo + 1);
        int i = lo, j = mid + 1, k = lo;
        while (i <= mid && j <= hi) {
            if (aux[i] <= aux[j]) arr[k++] = aux[i++];   // <= mantiene la estabilidad
            else arr[k++] = aux[j++];
        }
        while (i <= mid) arr[k++] = aux[i++];
        while (j <= hi) arr[k++] = aux[j++];
    }

    // ------------------------------------------------------------ Heap Sort
    public static void heapSort(int[] arr) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    private static void heapify(int[] arr, int n, int i) {
        while (true) {
            int mayor = i, l = 2 * i + 1, r = l + 1;
            if (l < n && arr[l] > arr[mayor]) mayor = l;
            if (r < n && arr[r] > arr[mayor]) mayor = r;
            if (mayor == i) return;
            swap(arr, i, mayor);
            i = mayor;
        }
    }
}
