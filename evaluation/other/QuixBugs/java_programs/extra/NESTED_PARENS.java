//Corrected package name from quixey to java_programs.extra;
//package quixey;
package java_programs.extra;
import java.util.*;

public class NESTED_PARENS {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        String S = in.next();
        int[] num = new int[S.length()];
        for(int i=0; i<S.length(); i++)
            num[i] = S.charAt(i)=='(' ? 1 : -1;

        System.out.println(is_properly_nested(num)==1 ? "GOOD" : "BAD");
    }

    public static int is_properly_nested(int[] A) {
        int bad = 0;
        int depth = 0;
        int i = 0;
        while(i < A.length) {
            depth += A[i];
            if(depth < 0) { bad = 1; }
            i+=1;
        }
        if(bad==0) return 1;
        else return 0;
    }
}
