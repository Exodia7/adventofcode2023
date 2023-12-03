
INPUT_FILE = "input.txt"

DEBUG = False

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    
    gearRatios = []
    
    i = 0
    while (i < len(lines)):
        j = 0
        while (j < len(lines[i])):
            if (lines[i][j] == '*'):
                # search all numbers that are around this gear
                gearNumbers = []
                i2 = max(i-1, 0)    # make sure we don't go negative
                while (len(gearNumbers) <= 2 and i2 <= i+1 and i2 < len(lines)):
                    j2 = max(j-1, 0)
                    while (len(gearNumbers) <= 2 and j2 <= j+1 and j2 < len(lines[i2])):
                        if (lines[i2][j2].isdigit()):
                            # we found a number
                            # search its start
                            start = j2
                            while (start > 0 and lines[i2][start-1].isdigit()):
                                start -= 1
                            # search the number's end
                            end = j2
                            while (end < len(lines[i2])-1 and lines[i2][end+1].isdigit()):
                                end += 1
                            
                            # and add this number to its gearNumbers
                            gearNum = int(lines[i2][start:end+1])
                            gearNumbers.append(gearNum)
                            
                            # finally, increase j2 to after the number
                            j2 = end+1
                        else:
                            j2 += 1
                    i2 += 1
                
                # now, if the number is a gear (EXACTLY 2 numbers around),
                if len(gearNumbers) == 2:
                    gearRatio = gearNumbers[0] * gearNumbers[1]
                    gearRatios.append(gearRatio)
            
            j += 1
        i += 1
    
    print(f"The sum of all gear ratios is: {sum(gearRatios)}")
    # ANSWER: 84159075