//Corrected package name from quixey to java_programs.extra;
//package quixey;
package java_programs.extra;

import java.util.*;

public class BINARY_SEARCH {
    public static int findFirstInSorted(int[] arr, int x) {
        int lo = 0;
        int hi = arr.length;

        while (lo <= hi) {
            int mid = (lo + hi) / 2;

            if (x == arr[mid] && (mid == 0 || x != arr[mid - 1])) {
                return mid;
            } else if (x <= arr[mid]) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return -1;
    }
}
