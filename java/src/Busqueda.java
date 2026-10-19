/**
 * Algoritmos de búsqueda del Punto 2. Todos devuelven el índice de x o -1.
 * Fuente principal: GeeksforGeeks (la URL de cada algoritmo está en su comentario).
 * La versión de Python (python/busqueda.py) es una traducción línea a línea de este archivo.
 */
public class Busqueda {

    // https://www.geeksforgeeks.org/dsa/linear-search/
    public static int lineal(int[] arr, int x) {
        for (int i = 0; i < arr.length; i++) if (arr[i] == x) return i;
        return -1;
    }

    // https://www.geeksforgeeks.org/dsa/binary-search/ (versión iterativa)
    public static int binaria(int[] arr, int x) {
        return binaria(arr, x, 0, arr.length - 1);
    }

    static int binaria(int[] arr, int x, int low, int high) {
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == x) return mid;
            if (arr[mid] < x) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }

    // https://www.geeksforgeeks.org/dsa/ternary-search/ (versión iterativa)
    public static int ternaria(int[] arr, int x) {
        int l = 0, r = arr.length - 1;
        while (r >= l) {
            int mid1 = l + (r - l) / 3;
            int mid2 = r - (r - l) / 3;
            if (arr[mid1] == x) return mid1;
            if (arr[mid2] == x) return mid2;
            if (x < arr[mid1]) r = mid1 - 1;
            else if (x > arr[mid2]) l = mid2 + 1;
            else {
                l = mid1 + 1;
                r = mid2 - 1;
            }
        }
        return -1;
    }

    // https://www.geeksforgeeks.org/dsa/jump-search/  (salto = raíz de n)
    public static int saltos(int[] arr, int x) {
        int n = arr.length;
        int step = (int) Math.floor(Math.sqrt(n));
        int prev = 0;
        while (arr[Math.min(step, n) - 1] < x) {
            prev = step;
            step += (int) Math.floor(Math.sqrt(n));
            if (prev >= n) return -1;
        }
        while (arr[prev] < x) {
            prev++;
            if (prev == Math.min(step, n)) return -1;
        }
        if (arr[prev] == x) return prev;
        return -1;
    }

    // https://www.geeksforgeeks.org/dsa/interpolation-search/
    // Se usa long en la fórmula para evitar desbordamiento ((x - lo) * (hi - lo) llega a ~9e13)
    // y se protege la división cuando arr[hi] == arr[lo] (valores repetidos).
    public static int interpolacion(int[] arr, int x) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi && x >= arr[lo] && x <= arr[hi]) {
            if (arr[hi] == arr[lo]) return arr[lo] == x ? lo : -1;
            int pos = lo + (int) (((long) (hi - lo) * ((long) x - arr[lo])) / ((long) arr[hi] - arr[lo]));
            if (arr[pos] == x) return pos;
            if (arr[pos] < x) lo = pos + 1;
            else hi = pos - 1;
        }
        return -1;
    }

    // https://www.geeksforgeeks.org/dsa/exponential-search/
    public static int exponencial(int[] arr, int x) {
        int n = arr.length;
        if (arr[0] == x) return 0;
        int i = 1;
        while (i < n && arr[i] <= x) i = i * 2;
        return binaria(arr, x, i / 2, Math.min(i, n - 1));
    }
}
