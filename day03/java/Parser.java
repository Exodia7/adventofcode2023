import java.util.List;

public class Parser {
    public Parser() {
    }
    
    public SchematicPart1 part1Parse(List<String> input) {
        SchematicPart1 schema = new SchematicPart1();
        
        // iterate over the lines
        for (int i=0; i < input.size(); i ++) {
            // iterate over the characters in the line
            String line = input.get(i);
            int j=0;
            while (j < line.length()) {
                if (Character.isDigit(line.charAt(j))) {
                    // search for the end of the number
                    int endOfNumber = j;
                    while (endOfNumber < line.length()-1 && Character.isDigit(line.charAt(endOfNumber+1))) {
                        endOfNumber ++;
                    }
                    // cast the number to int
                    int numValue = Integer.parseInt(line.substring(j, endOfNumber+1));
                    
                    // now, check if there is a special symbol around it
                    boolean isPartNumber = false;
                    int i2 = Math.max(0, i-1);
                    while (! isPartNumber && i2 < input.size() && i2 <= i+1) {
                        String inspectedLine = input.get(i2);
                        int j2 = Math.max(0, j-1);
                        while (! isPartNumber && j2 < inspectedLine.length() && j2 <= endOfNumber+1) {
                            char c = inspectedLine.charAt(j2);
                            if (! Character.isDigit(c) && c != '.') {
                                // there is a special symbol, hence it is a part number
                                isPartNumber = true;
                            }
                            else {
                                j2 ++;
                            }
                        }
                        
                        i2 ++;
                    }
                    
                    // create the number and add it to the Schematic
                    NumberPart1 n = new NumberPart1(numValue, isPartNumber);
                    schema.addNumber(n);
                    
                    // finally, increase j to past this number
                    j = endOfNumber + 1;
                }
                else {
                    // increase j to next character
                    j ++;
                }
            }
        }
        
        return schema;
    }
    
    public SchematicPart2 part2Parse(List<String> input) {
        SchematicPart2 schema = new SchematicPart2();
        
        // iterate over the lines
        for (int i=0; i < input.size(); i ++) {
            // iterate over the characters in the line
            String line = input.get(i);
            int j=0;
            while (j < line.length()) {
                if (line.charAt(j) != '.' && ! Character.isDigit(line.charAt(j))) {
                    Gear g = new Gear();
                    
                    // search for the adjacent numbers surrounding this index
                    int i2 = Math.max(0, i-1);
                    while (i2 < input.size() && i2 <= i+1) {
                        String inspectedLine = input.get(i2);
                        int j2 = Math.max(0, j-1);
                        while (j2 < inspectedLine.length() && j2 <= j+1) {
                            char c = inspectedLine.charAt(j2);
                            if (Character.isDigit(c)) {
                                // we found a number!
                                // find its starting point
                                int start = j2;
                                while (start > 0 && Character.isDigit(inspectedLine.charAt(start-1))) {
                                    start --;
                                }
                                // and find its ending point
                                int end = j2;
                                while (end < inspectedLine.length() - 1 && Character.isDigit(inspectedLine.charAt(end+1))) {
                                    end ++;
                                }
                                
                                // cast the number to int
                                int numValue = Integer.parseInt(inspectedLine.substring(start, end+1));
                                
                                // add it to the gear
                                g.addNumber(numValue);
                                
                                // and move j2 to the end of the number
                                j2 = end + 1;
                            }
                            else {
                                // move to next char
                                j2 ++;
                            }
                        }
                        // move to next line
                        i2 ++;
                    }
                    
                    // finally, add the candidate Gear to the schematic if it is truly a gear
                    if (g.size() == 2) {
                        schema.addGear(g);
                    }
                }
                
                j ++;
            }
        }
        
        return schema;
    }
}