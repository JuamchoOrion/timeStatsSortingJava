import java.util.ArrayList;
import java.util.List;

/**
 * Algoritmos de ordenamiento del Punto 1.
 * Fuente principal: GeeksforGeeks (la URL de cada algoritmo está en su comentario).
 * La versión de Python (python/ordenamiento.py) es una traducción línea a línea de este archivo.
 */
public class Ordenamiento {

    // ---------------------------------------------------------------
    // Insertion Sort
    // https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
    // ---------------------------------------------------------------
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // ---------------------------------------------------------------
    // Dual-Pivot QuickSort (pivotes: primer y último elemento)
    // https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/
    // ---------------------------------------------------------------
    public static void dualPivotQuickSort(int[] arr) {
        dualPivotQuickSort(arr, 0, arr.length - 1);
    }

    private static void dualPivotQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            int[] piv = partition(arr, low, high);
            dualPivotQuickSort(arr, low, piv[0] - 1);
            dualPivotQuickSort(arr, piv[0] + 1, piv[1] - 1);
            dualPivotQuickSort(arr, piv[1] + 1, high);
        }
    }

    private static int[] partition(int[] arr, int low, int high) {
        if (arr[low] > arr[high]) swap(arr, low, high);
        int j = low + 1;
        int g = high - 1, k = low + 1;
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

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // ---------------------------------------------------------------
    // Merge Sort
    // https://www.geeksforgeeks.org/dsa/merge-sort/
    // ---------------------------------------------------------------
    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    private static void merge(int[] arr, int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;
        int[] L = new int[n1];
        int[] R = new int[n2];
        for (int i = 0; i < n1; i++) L[i] = arr[l + i];
        for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) arr[k++] = L[i++];
            else arr[k++] = R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    // ---------------------------------------------------------------
    // Heap Sort
    // https://www.geeksforgeeks.org/dsa/heap-sort/
    // ---------------------------------------------------------------
    public static void heapSort(int[] arr) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    // Versión iterativa del heapify de GfG (misma lógica, sin recursión de cola)
    private static void heapify(int[] arr, int n, int i) {
        while (true) {
            int largest = i;
            int l = 2 * i + 1;
            int r = 2 * i + 2;
            if (l < n && arr[l] > arr[largest]) largest = l;
            if (r < n && arr[r] > arr[largest]) largest = r;
            if (largest == i) return;
            swap(arr, i, largest);
            i = largest;
        }
    }

    // ---------------------------------------------------------------
    // Radix Sort (LSD, base 10, counting sort estable por dígito)
    // https://www.geeksforgeeks.org/dsa/radix-sort/
    // ---------------------------------------------------------------
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
        for (int i = n - 1; i >= 0; i--) {
            int d = (arr[i] / exp) % 10;
            output[count[d] - 1] = arr[i];
            count[d]--;
        }
        System.arraycopy(output, 0, arr, 0, n);
    }

    // ---------------------------------------------------------------
    // Bucket Sort para enteros
    // https://www.geeksforgeeks.org/dsa/bucket-sort-2/
    // Se usan n cubetas. El valor x va a la cubeta
    //     idx = (x - min) * n / (max - min + 1)
    // de modo que el rango [min, max] se parte en n intervalos de igual ancho.
    // Cada cubeta se ordena con Insertion Sort (como en GfG) y luego se concatenan.
    // ---------------------------------------------------------------
    public static void bucketSort(int[] arr) {
        int n = arr.length;
        if (n == 0) return;
        int min = arr[0], max = arr[0];
        for (int v : arr) {
            if (v < min) min = v;
            if (v > max) max = v;
        }
        long rango = (long) max - min + 1;
        List<List<Integer>> buckets = new ArrayList<>(n);
        for (int i = 0; i < n; i++) buckets.add(new ArrayList<>());
        for (int v : arr) {
            int idx = (int) (((long) v - min) * n / rango);
            buckets.get(idx).add(v);
        }
        int k = 0;
        for (List<Integer> b : buckets) {
            insertionSortList(b);
            for (int v : b) arr[k++] = v;
        }
    }

    private static void insertionSortList(List<Integer> b) {
        for (int i = 1; i < b.size(); i++) {
            int key = b.get(i);
            int j = i - 1;
            while (j >= 0 && b.get(j) > key) {
                b.set(j + 1, b.get(j));
                j--;
            }
            b.set(j + 1, key);
        }
    }

    public static boolean estaOrdenado(int[] arr) {
        for (int i = 1; i < arr.length; i++) if (arr[i - 1] > arr[i]) return false;
        return true;
    }
}
