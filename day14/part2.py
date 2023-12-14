
import copy
from tqdm import tqdm

INPUT_FILE = "input.txt"
ROUND_ROCK = "O"
SQUARE_ROCK = "#"
EMPTY_SPACE = "."

NUM_CYCLES = 1000000000 # 1 billion

def moveRocksAroundOneCycle(data: [[str]]) -> [[str]]:
    """ Given the map with all the rocks, move all the round rocks
        around, first north, then west, then south, then east.
        Return the resulting map
    """
    # push rocks north, west, south, east
    data = moveAllRoundRocksVertically(data, "N")
    data = moveAllRoundRocksHorizontally(data, "W")
    data = moveAllRoundRocksVertically(data, "S")
    data = moveAllRoundRocksHorizontally(data, "E")
    # and return result
    return data

def moveAllRoundRocksVertically(data: [[str]], direction: str) -> [[str]]:
    """ Given the map with all the rocks, move all the round rocks
        in the given vertical direction ("N" for north, "S" for south). 
        Note that square rocks are fixed and will block round rocks.
    """
    # setup for the given direction
    match direction:
        case "N":   # = north
            # in the north case, we push round rocks from bottom (index len(data)-1) to top (index 0)
            lastRow = 0
            rowIterator = range(len(data)-1, -1, -1)
            previousRow = lambda n: n+1
        case "S":   # = south
            # in the south case, we push round rocks from top (index 0) to bottom (index len(data)-1)
            lastRow = len(data)-1
            rowIterator = range(len(data))
            previousRow = lambda n: n-1
    
    # propagate round rocks rolling in the given direction
    for col in range(len(data[0])):
        numRoundRocks = 0
        for row in rowIterator:
            match data[row][col]:
                case "O":   # = ROUND_ROCK
                    # count the number of round rocks
                    numRoundRocks += 1
                    # and take this round rock away
                    data[row][col] = EMPTY_SPACE
                case "#":   # = SQUARE_ROCK
                    # move all the accumulated round rocks here
                    destRow = previousRow(row)
                    while (numRoundRocks > 0):
                        # move one rock on destRow
                        data[destRow][col] = ROUND_ROCK
                        # move to the row before that
                        destRow = previousRow(destRow)
                        # decrease the remaining number of rocks to move
                        numRoundRocks -= 1
        # once we're done with one column, make sure to add the remaining round rocks again
        destRow = lastRow
        while (numRoundRocks > 0):
            # move one rock on destRow
            data[destRow][col] = ROUND_ROCK
            # move to the row before that
            destRow = previousRow(destRow)
            # decrease the remaining number of rocks to move
            numRoundRocks -= 1
    
    return data

def moveAllRoundRocksHorizontally(data: [[str]], direction: str) -> [[str]]:
    """ Given the map with all the rocks, move all the round rocks
        in the given horizontal direction ("W" for west, "E" for east). 
        Note that square rocks are fixed and will block round rocks.
    """
    # setup for the given direction
    match direction:
        case "W":   # = west
            # in the west case, we push round rocks from right (index len(data)-1) to left (index 0)
            lastCol = 0
            colIterator = range(len(data[0])-1, -1, -1)
            previousCol = lambda n: n+1
        case "E":   # = east
            # in the east case, we push round rocks from left (index 0) to right (index len(data)-1)
            lastCol = len(data[0])-1
            colIterator = range(len(data[0]))
            previousCol = lambda n: n-1
    
    # propagate round rocks rolling in the given direction
    for row in range(len(data)):
        numRoundRocks = 0
        for col in colIterator:
            match data[row][col]:
                case "O":   # = ROUND_ROCK
                    # count the number of round rocks
                    numRoundRocks += 1
                    # and take this round rock away
                    data[row][col] = EMPTY_SPACE
                case "#":   # = SQUARE_ROCK
                    # move all the accumulated round rocks here
                    destCol = previousCol(col)
                    while (numRoundRocks > 0):
                        # move one rock on destCol
                        data[row][destCol] = ROUND_ROCK
                        # move to the column before that
                        destCol = previousCol(destCol)
                        # decrease the remaining number of rocks to move
                        numRoundRocks -= 1
        # once we're done with one row, make sure to add the remaining round rocks again
        destCol = lastCol
        while (numRoundRocks > 0):
            # move one rock on destCol
            data[row][destCol] = ROUND_ROCK
            # move to the column before that
            destCol = previousCol(destCol)
            # decrease the remaining number of rocks to move
            numRoundRocks -= 1
    
    return data

def computeLoadOnNorth(data: [[str]]) -> int:
    """ Computes the total load caused by round rocks on the north beam
    """
    totalLoad = 0
    for row in range(len(data)):
        for col in range(len(data[row])):
            if (data[row][col] == ROUND_ROCK):
                # add the load of this round rock to the total load
                totalLoad += len(data) - row
    return totalLoad

def printMap(data: [[str]]):
    """ Prints the given map
    """
    for row in range(len(data)):
        for col in range(len(data[row])):
            print(data[row][col], end="")
        print()

def mapToStr(data: [[str]]) -> str:
    """ Transforms the given list representation of the map into a string representation of the same map
    """
    return "\n".join(["".join(row) for row in data])

def strToMap(data: str) -> [[str]]:
    """ Transforms the given string representation of the map into a list representation of the same map
    """
    return [[char for char in row] for row in data.split("\n")]



with open(INPUT_FILE, 'r') as f:
    DEBUG = False

    # parse the input data
    originalData = [[char for char in l.strip()] for l in f.readlines()]
    
    if (DEBUG):
        print("ORIGINAL MAP:")
        printMap(originalData)
        totalLoadNorthSide = computeLoadOnNorth(originalData)
        print(f"\nLoad on north beam = {totalLoadNorthSide}")
    
    # keep track of the resulting maps after each cycle
    dataIterations = {mapToStr(originalData): 0}
    currentData = copy.deepcopy(originalData)
    for i in range(NUM_CYCLES):
        # shuffle currentData around one cycle
        currentData = moveRocksAroundOneCycle(currentData)
        
        # check if we already had this exact configuration
        if (mapToStr(currentData) in dataIterations):
            # stop everything!!!
            # We found a loop!
            # based on the loop length, compute which element of the loop the "NUM_CYCLES" element will be
            
            # find where the loop starts and where it repeats, and deduce the loop length
            numCyclesLoopStart = dataIterations[mapToStr(currentData)]
            numCyclesRepeat = i+1
            loopLength = numCyclesRepeat - numCyclesLoopStart
            
            # we know that the loop starts after "numCyclesLoopStart" cycles, hence we can decrease that many cycles
            remainingNumCycles = NUM_CYCLES - numCyclesLoopStart
            # skip all the loops
            remainingNumCycles = remainingNumCycles % loopLength
            # and add back the few transitions before the loop to get the correct number of transitions of the map we are looking for
            remainingNumCycles += numCyclesLoopStart
            
            if (DEBUG):
                print(f"\n-------------------------\nFOUND A CYCLE!!! with map after {dataIterations[mapToStr(currentData)]} rotations")
                printMap(currentData)
                
                print(f"\nLoop has length {loopLength}, hence we just need to retrieve element after {remainingNumCycles}")
            
            # find the right element
            for element, cycleNum in dataIterations.items():
                if cycleNum == remainingNumCycles:
                    # overwrite currentData with it
                    currentData = strToMap(element)
                    # stop searching through the cycle elements
                    break
            
            if (DEBUG):
                print("RESULT MAP = ")
                printMap(currentData)
            
            # and exit the loop
            break
        else:
            # make a copy of the new map and save in dataIterations, along with the number of rotation cycles that were performed to reach this map configuration
            dataIterations[mapToStr(currentData)] = i+1
            
            if (DEBUG):
                print(f"\n-------------------------\nFOUND NEW MAP AFTER {i+1} rotations")
                printMap(currentData)
                totalLoadNorthSide = computeLoadOnNorth(currentData)
                print(f"\nLoad on north side = {totalLoadNorthSide}")
    
    # compute the load on the final map
    totalLoadNorthSide = computeLoadOnNorth(currentData)
    
    # print result
    print(f"The load on the north side after performing {NUM_CYCLES} cycles is {totalLoadNorthSide}")
    # ANSWER: 99118