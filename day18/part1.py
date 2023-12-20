
from typing import Union
import copy

INPUT_FILE = "test.txt"
DEBUG = False

def addNewColumnsToMap(map: list[list[bool]], index: int, numNewColumns: int) -> list[list[bool]]:
    """ Adds the specified number of new columns at the specified index in the map """
    defaultValue = False
    newMap = []
    for y in range(len(map)):
        newMap.append([])   # append a new row
        # add the elements before the new columns
        for x in range(index):
            newMap[y].append(map[y][x])
        # add the new column elements
        for i in range(numNewColumns):
            newMap[y].append(defaultValue)
        # and add the remaining elements after it
        for x in range(index, len(map[y])):
            newMap[y].append(map[y][x])
    
    return newMap

def addNewRowsToMap(map: list[list[bool]], index: int, numNewRows: int) -> list[list[bool]]:
    """ Adds the specified number of new rows at the specified index in the map """
    for i in range(numNewRows):
        map.insert(index, [False for j in range(len(map[0]))])
    return map

def performMove(pos: tuple[int], direction: str, numSteps: int) -> tuple[int]:
    """ Takes the given number of steps in the given direction and returns the resulting position """
    x, y = pos
    match direction:
        case "R":
            x += numSteps
        case "L":
            x -= numSteps
        case "D":
            y += numSteps
        case "U":
            y -= numSteps
    return (x, y)

def createMapWithBorderOf(data: list[list[Union[str, int]]]) -> list[list[bool]]:
    """ Given the instructions of moves, creates a map representing it, with tiles on the path having the value True, and all other tiles being False. """
    # initialize the map with just (0, 0)
    m = [[False]]
    currPos = (0, 0)
    startX = endX = startY = endY = 0
    for i in range(len(data)):
        # extract the next move to perform
        direction = data[i][0]
        numSteps = data[i][1]
        
        # compute the next position
        nextPos = performMove(currPos, direction, numSteps)
        nextX, nextY = nextPos
        
        if (DEBUG): print(f"Size of map: {len(m)}x{len(m[0])}, startX={startX}, endX={endX}, startY={startY}, endY={endY}")
        
        # then update the map according to this
        if (nextX < startX or endX < nextX):
            # add new columns
            numberColsToAdd = nextX-endX
            addColsIndex = 0
            startX = min(nextX, startX)
            if (endX < nextX):
                addColsIndex = endX+1
                endX = nextX
            m = addNewColumnsToMap(m, addColsIndex, numberColsToAdd)
        else:
            # add new rows
            numberRowsToAdd = nextY-endY
            addRowsIndex = 0
            startX = min(nextY, startY)
            if (endY < nextY):
                addRowsIndex = endY+1
                endY = nextY
            m = addNewRowsToMap(m, addRowsIndex, numberRowsToAdd)
        
        if (DEBUG): print(f"Size of map: {len(m)}x{len(m[0])}, startX={startX}, endX={endX}, startY={startY}, endY={endY}")
        
        # finally, mark the parts that are part of the border
        currX, currY = currPos
        for y in range(min(nextY, currY), max(nextY, currY)+1):
            for x in range(min(nextX, currX), max(nextX, currX)+1):
                m[y-startY][x-startX] = True
        
        # update currPos
        currPos = nextPos
    
    return m

def printBorders(bordersMap: list[list[bool]]):
    """ Prints the given map of borders """
    for y in range(len(bordersMap)):
        for x in range(len(bordersMap[y])):
            if bordersMap[y][x]:
                print("#", end='')
            else:
                print(".", end='')
        print()

def computeSpaceOccupiedBy(bordersMap: list[list[bool]]) -> int:
    """ Computes the size of the shape described by the edges given as parameter, including the edge lines """
    if (DEBUG): print(f"Size of map: {len(bordersMap)}x{len(bordersMap[0])}")
    
    totalSize = 0
    for y in range(len(bordersMap)):
        inside = False
        x = 0
        while (x < len(bordersMap[y])):
            if bordersMap[y][x]:
                # add one for this space
                totalSize += 1
                
                # continue up until the first empty space (or end of the line)
                while (x < len(bordersMap[y])-1 and bordersMap[y][x+1]):
                    totalSize += 1
                    x += 1
                
                # and then invert the side we are on
                inside = not inside
            
            elif inside:
                totalSize += 1
            
            x += 1
    
    return totalSize


    

with open(INPUT_FILE, 'r') as f:
    # 1) parse the data
    data = [l.strip().split(" ") for l in f.readlines()]
    for i in range(len(data)):
        # cast the number of steps to int
        data[i][1] = int(data[i][1])
        # remove the superfluous parts from the hex color
        data[i][2] = data[i][2][2:-1]
    
    # DEBUG
    if (DEBUG):
        print(data)
        print("\n----------------------\n")
    
    # 2) create the border
    borders = createMapWithBorderOf(data)
    
    # DEBUG
    #if (DEBUG):
    printBorders(borders)
    print("\n----------------------\n")
    
    # 3) compute how many tiles are on the border and inside
    terrainSize = computeSpaceOccupiedBy(borders)
    
    # 4) return the result
    print(f"Exactly {terrainSize} cubic meters of lava fit in the lagoon")
    # ANSWER: 