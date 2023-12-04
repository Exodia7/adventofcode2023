import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class SchematicPart2 {
    private List<Gear> gears;
    
    public SchematicPart2() {
        gears = new ArrayList<Gear>();
    }
    
    public SchematicPart2(List<Gear> gears) {
        this.gears = gears;
    }
    
    public void addGear(Gear g) {
        this.gears.add(g);
    }
    
    public Iterator<Gear> iterator() {
        return gears.iterator();
    }
}