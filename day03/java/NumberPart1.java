public class NumberPart1 {
    private boolean isPartNumber;
    private int value;
    
    public NumberPart1(int value, boolean isPartNumber) {
        this.value = value;
        this.isPartNumber = isPartNumber;
    }
    
    public boolean isPartNumber() {
        return this.isPartNumber;
    }
    
    public int getValue() {
        return this.value;
    }
}