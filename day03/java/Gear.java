import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class Gear {
    private List<Integer> adjacentNumbers;
    
    public Gear() {
        this.adjacentNumbers = new ArrayList<Integer>();
    }
    
    public void addNumber(Integer n) {
        adjacentNumbers.add(n);
    }
    
    public Iterator<Integer> iter() {
        return adjacentNumbers.iterator();
    }
    
    public int size() {
        return adjacentNumbers.size();
    }
}