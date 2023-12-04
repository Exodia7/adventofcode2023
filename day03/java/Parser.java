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
}