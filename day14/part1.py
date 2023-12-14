
import time

INPUT_FILE = "input.txt"
ROUND_ROCK = "O"
SQUARE_ROCK = "#"
EMPTY_SPACE = "."

def moveAllRoundRocksNorthV1(data: [[str]]) -> [[str]]:
    """ Given the map with all the rocks, move all the round rocks
        as far north as possible. Note that square rocks are fixed
        and will block round rocks.
        
        This method should be less efficient than V2
    """
    # check each row starting at 1 (no need for zero, as rocks there don't move further)
    for row in range(1, len(data)):
        for col in range(len(data[row])):
            if (data[row][col] == ROUND_ROCK):
                # move the rock upwards as far as it can
                destRow = row
                while (destRow > 0 and data[destRow-1][col] == EMPTY_SPACE):
                    destRow -= 1
                if (destRow != row):
                    # move the round rock, i.e. replace current position by an empty space
                    data[row][col] = EMPTY_SPACE
                    data[destRow][col] = ROUND_ROCK
    
    return data

def moveAllRoundRocksNorthV2(data: [[str]]) -> [[str]]:
    """ Given the map with all the rocks, move all the round rocks
        as far north as possible. Note that square rocks are fixed
        and will block round rocks.
        
        This method should be more efficient than V1
    """
    # propagate round rocks rolling from the south-most end towards the north --> allows to do a single pass
    for col in range(len(data[0])):
        numRoundRocks = 0
        for row in range(len(data)-1, -1, -1):
            match data[row][col]:
                case "O":   # = ROUND_ROCK
                    # count the number of round rocks
                    numRoundRocks += 1
                    # and take this round rock away
                    data[row][col] = EMPTY_SPACE
                case "#":   # = SQUARE_ROCK
                    # move all the accumulated round rocks here
                    destRow = row + 1
                    while (numRoundRocks > 0):
                        # move one rock on destRow
                        data[destRow][col] = ROUND_ROCK
                        # move to next row
                        destRow += 1
                        # decrease the remaining number of rocks to move
                        numRoundRocks -= 1
        # once we're done with one column, make sure to add the remaining round rocks again
        destRow = 0
        while (numRoundRocks > 0):
            # move one rock on destRow
            data[destRow][col] = ROUND_ROCK
            # move to next row
            destRow += 1
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


with open(INPUT_FILE, 'r') as f:
    # parse the input data
    originalData = [[char for char in l.strip()] for l in f.readlines()]
    
    # move all rocks up
    allNorthData = moveAllRoundRocksNorthV2(originalData)
    # ALTERNATIVE:
    #allNorthData = moveAllRoundRocksNorthV1(originalData)
    
    # compute the load
    totalLoadNorthSide = computeLoadOnNorth(allNorthData)
    
    # print result
    print(f"The load on the north side after rolling all round rocks upwards is {totalLoadNorthSide}")
    # ANSWER: 108792