import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class SchematicPart1 {
    private List<Number> numbers;
    
    public SchematicPart1() {
        numbers = new ArrayList<Number>();
    }
    
    public SchematicPart1(List<Number> numbers) {
        this.numbers = numbers;
    }
    
    public void addNumber(Number n) {
        this.numbers.add(n);
    }
    
    public Iterator<Number> iterator() {
        return numbers.iterator();
    }
}