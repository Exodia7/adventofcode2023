public class Number {
    private boolean isPartNumber;
    private int value;
    
    public Number(int value, boolean isPartNumber) {
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