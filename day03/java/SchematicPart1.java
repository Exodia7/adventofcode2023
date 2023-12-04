import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class SchematicPart1 {
    private List<NumberPart1> numbers;
    
    public SchematicPart1() {
        numbers = new ArrayList<NumberPart1>();
    }
    
    public SchematicPart1(List<NumberPart1> numbers) {
        this.numbers = numbers;
    }
    
    public void addNumber(NumberPart1 n) {
        this.numbers.add(n);
    }
    
    public Iterator<NumberPart1> iterator() {
        return numbers.iterator();
    }
}