
/**
 *  This program takes in an algorithm and runs the corresponding java program
 *  with the json test cases as input and gets the return value from the program.
 */

import java.util.*;
import java.lang.reflect.*;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java_programs.*;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonParser;
import com.google.gson.JsonElement;

public class JavaDeserialization {
    public static void main(String[] args) throws Exception {

        // Check if passing in proper arguments.
        if(args.length < 2)
        {
            System.out.println("Not enough arguments.");
            System.exit(0);
        }

        String methodName = args[0];
        String className = methodName.toUpperCase();

        // Get parameter type for class method.
        try {
            Class target_class = Class.forName("java_programs." + className);
            Method[] method = target_class.getDeclaredMethods();

            for (Method m : method) {
                if (!m.getName().equals(methodName)) {
                    continue;
                }

                Type[] types = m.getParameterTypes();
                Object[] parameters = getParameters(types, args);

                try {
                    String returnValue = String.valueOf(m.invoke(null, parameters));
                    System.out.println(returnValue);
                } catch (IllegalArgumentException e) {
                    System.out.println("Invalid parameters.: Mismatch types or wrong number of arguments.");
                }
            }
        } catch (ClassNotFoundException e) {
            System.out.println(className + " Class is not found.");
        } catch (Exception e) {
            // e.printStackTrace();
            System.out.println("nuu :( "+e.getCause());
        }
    }

    // Create list of objects corresponding to input arguments through deserialization
    public static Object[] getParameters(Type[] types,  String[] args) {
        int numOfParameters = types.length;
        Object[] parameters = new Object[numOfParameters];
        Gson gsonArguments = new Gson();
        try {
            if (numOfParameters == args.length - 1) {
                for (int i = 0; i < numOfParameters; i++) {
                    Type type = types[i];
                    parameters[i] = gsonArguments.fromJson(args[i + 1], (Class)type);
                    if (type.getTypeName().equals("java.util.ArrayList")) {
                        // workaround for reading in Integers and Doubles differently
                        // default is to read all Numbers as Doubles
                        JsonParser parser = new JsonParser();
                        JsonArray array = parser.parse(args[i + 1]).getAsJsonArray();

                        ArrayList checked_arr = new ArrayList();
                        for (int j = 0; j < array.size(); j++) {
                            JsonElement elem = array.get(j);
                            String str_elem = elem.getAsString();
                            if (str_elem.matches("[0-9]+")) {
                                checked_arr.add((Integer) elem.getAsInt());
                            } else if (str_elem.matches("[0-9]+.[0-9]+")) {
                                checked_arr.add(elem.getAsDouble());
                            } else {
                                checked_arr.add(str_elem);
                            }
                        }
                        parameters[i] = checked_arr;
                    } else {
                        parameters[i] = gsonArguments.fromJson(args[i + 1], (Class)type);
                    }
                }
            }

        } catch (NumberFormatException e){
            System.out.println("Incompatible types: Object cannot be converted.");
        }
        return parameters;
    }

}
