package java_testcases;
import java.util.*;

import java_programs.Node;
import java_programs.REVERSE_LINKED_LIST;

/**
 * Driver to test revers linked list.
 */
public class REVERSE_LINKED_LIST_TEST {
    public static void main(String[] args) throws Exception {
        // Case 1: 5-node list input
        // Expected Good Output: Reversed!  1 2 3 4 5
        Node node1 = new Node("1");
        Node node2 = new Node("2", node1);
        Node node3 = new Node("3", node2);
        Node node4 = new Node("4", node3);
        Node node5 = new Node("5", node4);

        Node result = REVERSE_LINKED_LIST.reverse_linked_list(node5);

        if (result.getValue() == node1.getValue()) {
            System.out.printf("Reversed! ");
        } else {
            System.out.printf("Not Reversed! ");
        }
        while (result != null) {
            System.out.printf("%s ", result.getValue());
            result = result.getSuccessor();
        }
        System.out.println();

        // Case 2: 1-node list input
        // Expected Output: Reversed!  0
        Node node = new Node("0");
        result = REVERSE_LINKED_LIST.reverse_linked_list(node);

        if (result.getValue() == node.getValue()) {
            System.out.printf("Reversed! ");
        } else {
            System.out.printf("Not Reversed! ");
        }
        while (result != null) {
            System.out.printf("%s ", result.getValue());
            result = result.getSuccessor();
        }
        System.out.println();

        // Case 3: None input
        // Expected Output: None
        result = REVERSE_LINKED_LIST.reverse_linked_list(null);

        if (result == null) {
            System.out.printf("Reversed! ");
        } else {
            System.out.printf("Not Reversed! ");
        }
        while (result != null) {
            System.out.printf("%s ", result.getValue());
            result = result.getSuccessor();
        }
        System.out.println();

    }
}