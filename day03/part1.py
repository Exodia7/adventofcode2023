
INPUT_FILE = "input.txt"

DEBUG = False

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    
    partNumbers = []
    
    i = 0
    while (i < len(lines)):
        j = 0
        while (j < len(lines[i])):
            if (lines[i][j].isdigit()):
                # search until where the number goes
                endOfNumber = j+1
                while (endOfNumber < len(lines[i]) and lines[i][endOfNumber].isdigit()):    # and lines[i][endOfNumber] != '.'):
                    endOfNumber += 1
                
                if DEBUG: print(f"DEBUG - At index i={i}, j={j}, found number going until index {endOfNumber}")
                
                # then check if there's any special character around the number
                isPartNumber = False
                i2 = max(i-1, 0)    # make sure we don't go negative
                while (not isPartNumber and i2 < i+2 and i2 < len(lines)):
                    j2 = max(j-1, 0)
                    while (not isPartNumber and j2 <= endOfNumber and j2 < len(lines[i2])):
                        if (lines[i2][j2] != '.' and not lines[i2][j2].isalnum()):
                            # we found a special character
                            isPartNumber = True
                        j2 += 1
                    i2 += 1
                
                if DEBUG: print(f"DEBUG - The number is {'NOT' if not isPartNumber else ''} a part number!")
                
                # now, if the number is a part number,
                if isPartNumber:
                    num = int(lines[i][j:endOfNumber])
                    partNumbers.append(num)
                
                # and increase j to just after the number
                j = endOfNumber
            else:
                j += 1
        i += 1
    
    if DEBUG: print(f"The part numbers are: {partNumbers}")
    
    print(f"The sum of all part numbers is: {sum(partNumbers)}")
    # ANSWER: 539713