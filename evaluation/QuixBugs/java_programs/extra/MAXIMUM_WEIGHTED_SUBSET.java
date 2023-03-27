//Corrected package name from quixey to java_programs.extra;
//package quixey;
package java_programs.extra;
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author derricklin
 */
public class MAXIMUM_WEIGHTED_SUBSET {
    public static int maxSubsetWeight(int[] weights, int bound) {
        if (weights.length == 0) {
            return 0;
        }
        int[][] maxWeight = new int[weights.length][bound];
        for (int w = 0; w <= bound; w++)
            maxWeight[0][w] = weights[0] <= w ? weights[0] : 0;

        for (int i = 1; i < weights.length; i++) {
            for (int w = 0; w <= bound; w++) {
                if (weights[i] > w) {
                    maxWeight[i][w] = maxWeight[i-1][w];
                } else {
                    int include = weights[i] + maxWeight[i-1][w - weights[i]];
                    int exclude = maxWeight[i-1][w];
                    maxWeight[i][w] = Math.max(include, exclude);
                }
            }
        }
        return maxWeight[weights.length-1][bound];
    }
}
