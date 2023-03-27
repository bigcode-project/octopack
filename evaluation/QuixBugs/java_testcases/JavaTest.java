package java_testcases;
import java.util.*;

import java_programs.BREADTH_FIRST_SEARCH;
import java_programs.DEPTH_FIRST_SEARCH;
import java_programs.DETECT_CYCLE;
import java_programs.MINIMUM_SPANNING_TREE;
import java_programs.Node;
import java_programs.REVERSE_LINKED_LIST;
import java_programs.SHORTEST_PATHS;
import java_programs.SHORTEST_PATH_LENGTHS;
import java_programs.WeightedEdge;

public class JavaTest {
    public static void main(String[] args) throws Exception {
        Node station1 = new Node("Westminster", new ArrayList<Node>());
        Node station2 = new Node("Waterloo", new ArrayList<Node>(Arrays.asList(station1)));
        Node station3 = new Node("Trafalgar Square",  new ArrayList<Node>(Arrays.asList(station1, station2)));
        Node station4 = new Node("Canary Wharf",  new ArrayList<Node>(Arrays.asList(station2, station3)));
        Node station5 = new Node("London Bridge",  new ArrayList<Node>(Arrays.asList(station4, station3)));
        Node station6 = new Node("Tottenham Court Road",  new ArrayList<Node>(Arrays.asList(station5, station4)));

        if (BREADTH_FIRST_SEARCH.breadth_first_search(station6, station1))
            System.out.println("Path Found!");
        else
            System.out.println("Path Not Found!");

        DEPTH_FIRST_SEARCH dfs = new DEPTH_FIRST_SEARCH();

        if (dfs.depth_first_search(station6, station1))
            System.out.println("Path Found!");
        else
            System.out.println("Path Not Found!");

        Node node1 = new Node("1");
        Node node2 = new Node("2", node1);
        Node node3 = new Node("3", node2);
        Node node4 = new Node("4", node3);
        Node node5 = new Node("5", node4);

        Node result = REVERSE_LINKED_LIST.reverse_linked_list(node5);

        //TODO: handle a null pointer exception
        if (result.getValue() == node1.getValue()) {
            System.out.println("Reversed!");
        }

        while (result != null) {
            System.out.printf("%s ", result.getValue());
            result = result.getSuccessor();
        }
        System.out.println();

        node1.setSuccessor(node2);

        if (DETECT_CYCLE.detect_cycle(node5)) {
            System.out.println("Cycle detected!");
        } else {
            System.out.println("Cycle not detected!");
        }

        WeightedEdge edge1 = new WeightedEdge(node1, node2, 10);
        WeightedEdge edge2 = new WeightedEdge(node2, node3, 15);
        WeightedEdge edge3 = new WeightedEdge(node3, node4, 10);
        WeightedEdge edge4 = new WeightedEdge(node1, node4, 10);

        List<WeightedEdge> graph = new ArrayList<>(Arrays.asList(edge1, edge2, edge3, edge4));

        Set<WeightedEdge> minspantree = new HashSet<>();
        minspantree.addAll(MINIMUM_SPANNING_TREE.minimum_spanning_tree(graph));

        for (WeightedEdge edge : minspantree) {
            System.out.printf("u: %s, v: %s, weight: %d\n", edge.node1.getValue(), edge.node2.getValue(), edge.weight);
        }

        Node nodeA = new Node("A");
        WeightedEdge edge_1 = new WeightedEdge(nodeA, new Node("B"), 3);
        WeightedEdge edge_2 = new WeightedEdge(nodeA, new Node("C"), 3);
        WeightedEdge edge_3 = new WeightedEdge(nodeA, new Node("F"), 5);
        WeightedEdge edge_4 = new WeightedEdge(new Node("C"), new Node("B"), -2);
        WeightedEdge edge_5 = new WeightedEdge(new Node("C"), new Node("D"), 7);
        WeightedEdge edge_6 = new WeightedEdge(new Node("C"), new Node("E"), 4);
        WeightedEdge edge_7 = new WeightedEdge(new Node("D"), new Node("E"), -5);
        WeightedEdge edge_8 = new WeightedEdge(new Node("E"), new Node("F"), -1);

        
        List<WeightedEdge> graph1 = new ArrayList<>(Arrays.asList(edge_1, edge_2, edge_3, edge_4, edge_5, edge_6, edge_7, edge_8));

        Map<String,Integer> weight_by_node = new HashMap<String,Integer>();
        weight_by_node = SHORTEST_PATHS.shortest_paths(nodeA, graph1);
        for (String node : weight_by_node.keySet()) {
            System.out.printf("Node: %s, distance: %d\n", node, weight_by_node.get(node));
        }


        Map<List<String>, Integer> graph2 = new HashMap<>();
        graph2.put(new ArrayList<String>(Arrays.asList("A","C")),3);
        graph2.put(new ArrayList<String>(Arrays.asList("A","F")),5);
        graph2.put(new ArrayList<String>(Arrays.asList("C","B")),-2);
        graph2.put(new ArrayList<String>(Arrays.asList("C","D")),7);
        graph2.put(new ArrayList<String>(Arrays.asList("C","E")),4);
        graph2.put(new ArrayList<String>(Arrays.asList("D","E")),-5);
        graph2.put(new ArrayList<String>(Arrays.asList("E","F")),-1);
       
        //Removed existed variable name path
        //SHORTEST_PATHS path = new SHORTEST_PATHS();
        
        //Removed existed variable name weight_by_node
        //Map<String,Integer> weight_by_node = new HashMap<String,Integer>();
        weight_by_node = SHORTEST_PATHS.shortest_paths("A", graph2);
        for (String node : weight_by_node.keySet()) {
            System.out.printf("Node: %s, distance: %d\n", node, weight_by_node.get(node));
        }

        Map<List<Integer>, Integer> graph3 = new HashMap<>();
        graph3.put(new ArrayList<Integer>(Arrays.asList(1,3)),3);
        graph3.put(new ArrayList<Integer>(Arrays.asList(1,6)),5);
        graph3.put(new ArrayList<Integer>(Arrays.asList(3,2)),-2);
        graph3.put(new ArrayList<Integer>(Arrays.asList(3,4)),7);
        graph3.put(new ArrayList<Integer>(Arrays.asList(3,5)),4);
        graph3.put(new ArrayList<Integer>(Arrays.asList(4,5)),-5);
        graph3.put(new ArrayList<Integer>(Arrays.asList(5,6)),-1);

        Map<List<Integer>,Integer> length_by_path = new HashMap<>();
        length_by_path = SHORTEST_PATH_LENGTHS.shortest_path_lengths(6, graph3);
        for (List<Integer> edge : length_by_path.keySet()) {
            for(Integer i : edge) {
                System.out.printf(" Node: %d ", i);
            }
            System.out.printf(" %d\n",  length_by_path.get(edge));
        }
    }
}