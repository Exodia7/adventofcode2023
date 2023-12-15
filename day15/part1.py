
INPUT_FILE = "input.txt"

def HASH(s : str) -> int:
    """ Holiday ASCII String Helper:
        Transforms any string into a number in the range 0-255
    """
    currentVal = 0
    for char in s:
        asciiCode = ord(char)
        currentVal = (17 * (currentVal + asciiCode)) % 256
        ''' # STEP BY STEP ALTERNATIVE:
        asciiCode = ord(char)
        currentVal += asciiCode
        currentVal *= 17
        currentVal = currentVal % 256
        '''
    return currentVal

with open(INPUT_FILE, 'r') as f:
    # parse the input data
    data = f.readline().strip().split(",")
    
    # compute the HASH value of each step
    total = 0
    for step in data:
        total += HASH(step)
    
    # return the sum
    print(f"The sum of the results of the HASH algorithm on all steps is: {total}")
    # ANSWER: 506891