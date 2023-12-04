import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;
import java.io.FileNotFoundException;

public class Day03 {
    public static void main(String[] args) {
        boolean wrongInput = false;
        boolean runPart1 = false;
        boolean runPart2 = false;
        if (args.length > 0) {
            int i=0;
            while (i < args.length && !wrongInput && (!runPart1 || !runPart2)) {
                // parse next item
                if (args[i].equals("1")) {
                    runPart1 = true;
                }
                else if (args[i].equals("2")) {
                    runPart2 = true;
                }
                else {
                    wrongInput = true;
                }
                i ++;
            }
        }
        else {
            wrongInput = true;
        }
        
        if (wrongInput) {
            System.out.println("Please provide 1 argument when running this, which should indicate which part of the challenge you would like to run:");
            System.out.println(" - '1': executes part 1 of the challenge");
            System.out.println(" - '2': executes part 2 of the challenge");
        }
        else {
            if (runPart1) {
                System.out.println("\nExecuting Part1: ");
                part1();
            }
            if (runPart2) {
                System.out.println("\nExecuting Part2: ");
                part2();
            }
        }
    }
    
    public static void part1() {
        // read the input file
        String INPUT_FILE = "input.txt";
        try {
            BufferedReader reader = new BufferedReader(new FileReader(INPUT_FILE));
            List<String> lines = reader.lines().collect(Collectors.toList());
            
        
            // parse it to a Schematic
            Parser parser = new Parser();
            SchematicPart1 schema = parser.part1Parse(lines);
            
            // then, compute the sum of all the part numbers
            int partNumSum = 0;
            Iterator<NumberPart1> iter = schema.iterator();
            while (iter.hasNext()) {
                NumberPart1 nextNum = iter.next();
                
                if (nextNum.isPartNumber()) {
                    partNumSum += nextNum.getValue();
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
    
    public static void part2() {
        // read the input file
        String INPUT_FILE = "input.txt";
        try {
            BufferedReader reader = new BufferedReader(new FileReader(INPUT_FILE));
            List<String> lines = reader.lines().collect(Collectors.toList());
            
        
            // parse it to a Schematic
            Parser parser = new Parser();
            SchematicPart2 schema = parser.part2Parse(lines);
            
            // then, compute the sum of all the gear ratios
            int gearRatioSum = 0;
            Iterator<Gear> iter = schema.iterator();
            while (iter.hasNext()) {
                Gear nextGear = iter.next();
                
                // compute its gear ratio
                Iterator<Integer> iter2 = nextGear.iter();
                int gearRatio = iter2.next() * iter2.next();
                
                // and add it to the total sum
                gearRatioSum += gearRatio;
            }
            
            // and print the result
            System.out.println("The sum of all the gear ratios is: " + gearRatioSum);
        }
        catch (FileNotFoundException e) {
            System.out.println("Error: Could not find file '" + INPUT_FILE + "'");
        }
        
        // ANSWER: 84159075
    }
}