/**
 * Algoritmos de búsqueda del Punto 2. Todos reciben un arreglo ORDENADO
 * ascendente (excepto la lineal, que sirve con cualquiera) y devuelven el
 * índice donde está la clave, o -1 si no está.
 *
 * Fuentes base (GeeksforGeeks), verificar que los enlaces sigan vigentes:
 *   Lineal:        https://www.geeksforgeeks.org/linear-search/
 *   Binaria:       https://www.geeksforgeeks.org/binary-search/
 *   Ternaria:      https://www.geeksforgeeks.org/ternary-search/
 *   Saltos:        https://www.geeksforgeeks.org/jump-search/
 *   Interpolación: https://www.geeksforgeeks.org/interpolation-search/
 *   Exponencial:   https://www.geeksforgeeks.org/exponential-search/
 * Todas se escribieron de forma iterativa para evitar diferencias por
 * recursión entre Java y Python. La versión de Python (busquedas.py) tiene
 * exactamente la misma estructura.
 */
public class Busquedas {

    /** Lineal: recorre de izquierda a derecha hasta encontrar la clave. */
    public static int lineal(int[] a, int clave) {
        for (int i = 0; i < a.length; i++) {
            if (a[i] == clave) return i;
        }
        return -1;
    }

    /** Binaria iterativa. */
    public static int binaria(int[] a, int clave) {
        return binariaRango(a, clave, 0, a.length - 1);
    }

    private static int binariaRango(int[] a, int clave, int lo, int hi) {
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == clave) return mid;
            if (a[mid] < clave) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    /** Ternaria iterativa: dos puntos medios, tres zonas. */
    public static int ternaria(int[] a, int clave) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            int tercio = (hi - lo) / 3;
            int m1 = lo + tercio;
            int m2 = hi - tercio;
            if (a[m1] == clave) return m1;
            if (a[m2] == clave) return m2;
            if (clave < a[m1]) {
                hi = m1 - 1;
            } else if (clave > a[m2]) {
                lo = m2 + 1;
            } else {
                lo = m1 + 1;
                hi = m2 - 1;
            }
        }
        return -1;
    }

    /** Saltos (Jump Search): bloques de tamaño floor(sqrt(n)) y luego lineal dentro del bloque. */
    public static int saltos(int[] a, int clave) {
        int n = a.length;
        if (n == 0) return -1;
        int paso = (int) Math.sqrt(n);
        if (paso < 1) paso = 1;
        int previo = 0;
        int actual = paso;
        // Avanzar por bloques mientras el último elemento del bloque sea menor que la clave.
        while (a[Math.min(actual, n) - 1] < clave) {
            previo = actual;
            actual += paso;
            if (previo >= n) return -1;
        }
        // Búsqueda lineal dentro del bloque [previo, min(actual, n)).
        int fin = Math.min(actual, n);
        for (int i = previo; i < fin; i++) {
            if (a[i] == clave) return i;
            if (a[i] > clave) return -1;
        }
        return -1;
    }

    /** Interpolación: estima la posición según el valor de la clave. */
    public static int interpolacion(int[] a, int clave) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi && clave >= a[lo] && clave <= a[hi]) {
            if (a[hi] == a[lo]) {                 // evita división por cero
                return a[lo] == clave ? lo : -1;
            }
            // Producto en long: (clave - a[lo]) * (hi - lo) puede superar 2^31.
            int pos = lo + (int) (((long) (clave - a[lo]) * (hi - lo)) / (a[hi] - a[lo]));
            if (a[pos] == clave) return pos;
            if (a[pos] < clave) lo = pos + 1;
            else hi = pos - 1;
        }
        return -1;
    }

    /** Exponencial: duplica el límite (1, 2, 4, ...) y luego busca binariamente en ese rango. */
    public static int exponencial(int[] a, int clave) {
        int n = a.length;
        if (n == 0) return -1;
        if (a[0] == clave) return 0;
        int i = 1;
        while (i < n && a[i] <= clave) {
            i *= 2;
        }
        return binariaRango(a, clave, i / 2, Math.min(i, n - 1));
    }
}
