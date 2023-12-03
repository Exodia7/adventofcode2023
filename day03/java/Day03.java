import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;
import java.io.FileNotFoundException;

public class Day03 {
    public static void main(String[] args) {
        part1();
    }
    
    public static void part1() {
        // read the input file
        String INPUT_FILE = "input.txt";
        try {
            BufferedReader reader = new BufferedReader(new FileReader(INPUT_FILE));
            List<String> lines = reader.lines().collect(Collectors.toList());
            
        
            // parse it to a Schematic
            Parser parser = new Parser();
            Schematic schema = parser.part1Parse(lines);
            
            // then, compute the sum of all the part numbers
            int partNumSum = 0;
            Iterator<Number> iter = schema.iterator();
            while (iter.hasNext()) {
                Number nextNum = iter.next();
                
                System.out.print("Found number with value " + nextNum.getValue() + " who is");
                
                if (nextNum.isPartNumber()) {
                    System.out.println(" a part number!");
                    partNumSum += nextNum.getValue();
                }
                else {
                    System.out.println(" NOT a part number");
                }
            }
            
            // and print the result
            System.out.println("The sum of all the part numbers is: " + partNumSum);
        }
        catch (FileNotFoundException e) {
            System.out.println("Error: Could not find file '" + INPUT_FILE + "'");
        }
        
        // ANSWER: 539713
    }
}