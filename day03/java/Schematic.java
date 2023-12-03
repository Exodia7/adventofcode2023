import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class Schematic {
    private List<Number> numbers;
    
    public Schematic() {
        numbers = new ArrayList<Number>();
    }
    
    public Schematic(List<Number> numbers) {
        this.numbers = numbers;
    }
    
    public void addNumber(Number n) {
        this.numbers.add(n);
    }
    
    public Iterator<Number> iterator() {
        return numbers.iterator();
    }
}