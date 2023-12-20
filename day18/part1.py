
from typing import Union
import copy

INPUT_FILE = "input.txt"

BOTTOM_LEFT_CORNER = "L"
BOTTOM_RIGHT_CORNER = "J"
TOP_LEFT_CORNER = "F"
TOP_RIGHT_CORNER = "7"
VERTICAL_CONNECT = "|"
HORIZONTAL_CONNECT = "-"
NO_CONNECT = "."

DEBUG = False


def generateEdgesFromMoves(data: list[list[Union[str, int]]]) -> list[tuple[int]]:
    """ Based on the given moves to perform, returns a list of the positions of the edges """
    currPos = (0, 0)
    edges = [(0, 0)]
    for i in range(len(data)):
        # extract the next move to perform
        direction = data[i][0]
        numSteps = data[i][1]
        # perform it to get the destination position
        nextPos = performMove(currPos, direction, numSteps)
        
        # DEBUG
        #if (DEBUG): print(f"Moving from {currPos} to {nextPos}")
        
        # add the new border to the list
        edges.append(nextPos)
        
        # finally, update the current position
        currPos = nextPos
    
    return edges

def addNewColumnsToMap(map: list[list[bool]], index: int, numNewColumns: int) -> list[list[bool]]:
    """ Adds the specified number of new columns at the specified index in the map """
    if (DEBUG): print(f"Adding {numNewColumns} columns at index {index}")
    
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
    if (DEBUG): print(f"Adding {numNewRows} rows at index {index}")
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

def createMapWithBorderOf(edges: list[tuple[int]]) -> list[list[bool]]:
    """ Given the edges, creates a map representing it, with tiles on the path having the value True, and all other tiles being False. """
    # find the dimensions in X and Y
    maxX, maxY = edges[0]
    for i in range(1, len(edges)):
        currX, currY = edges[i]
        if (maxX < currX):
            maxX = currX
        if (maxY < currY):
            maxY = currY
    # initialize the map with just False values
    m = [[False for x in range(maxX+1)] for y in range(maxY+1)]
    currPos = edges[0]
    for i in range(1, len(edges)):
        # get the next edge
        nextPos = edges[i]
        
        # set all spaces between the current and the next to the value True
        currX, currY = currPos
        nextX, nextY = nextPos
        for y in range(min(currY, nextY), max(currY, nextY)+1):
            for x in range(min(currX, nextX), max(currX, nextX)+1):
                m[y][x] = True
        
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

def computeConnector(bordersMap: list[list[bool]], pos: tuple[int]) -> str:
    """ Computes what type of connecting piece this position would be """
    x, y = pos
    
    # Check which of the sides is connected from top, bottom, left, right
    isTopConnected = False 
    if (y > 0): isTopConnected = bordersMap[y-1][x]
    isBottomConnected = False
    if (y < len(bordersMap)-1): isBottomConnected = bordersMap[y+1][x]
    isLeftConnected = False
    if (x > 0): isLeftConnected = bordersMap[y][x-1]
    isRightConnected = False
    if (x < len(bordersMap[0])-1): isRightConnected = bordersMap[y][x+1]
    
    # return the correct symbol
    if (isTopConnected and isRightConnected):
        return BOTTOM_LEFT_CORNER
    elif (isTopConnected and isLeftConnected):
        return BOTTOM_RIGHT_CORNER
    elif (isBottomConnected and isRightConnected):
        return TOP_LEFT_CORNER
    elif (isBottomConnected and isLeftConnected):
        return TOP_RIGHT_CORNER
    elif (isTopConnected and isTopConnected):
        return VERTICAL_CONNECT
    elif (isLeftConnected and isRightConnected):
        return HORIZONTAL_CONNECT
    else:
        return NO_CONNECT

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
                ''' NOTE: the logic for this, computing if we're inside or not, 
                    is largely based on part2.py of day10
                '''
                startConnector = computeConnector(bordersMap, (x, y))
                
                if startConnector == VERTICAL_CONNECT:
                    # in case we cross a vertical border, we go from inside to outside or the other way around
                    inside = not inside
                else:
                    # we have a corner, so it's more complex
                    sameSideIsOnSide = "left"   # should be a TOP_LEFT_CORNER
                    if startConnector == BOTTOM_LEFT_CORNER:
                        sameSideIsOnSide = "right"
                    
                    # continue up until the first empty space (or end of the line)
                    while (x < len(bordersMap[y])-1 and bordersMap[y][x+1]):
                        totalSize += 1
                        x += 1
                    endConnector = computeConnector(bordersMap, (x, y))
                    
                    # and then check if we remain on the same side or not
                    if ((endConnector == BOTTOM_RIGHT_CORNER and sameSideIsOnSide != "right") 
                        or 
                        (endConnector == TOP_RIGHT_CORNER and sameSideIsOnSide != "left")):
                        # invert whether we're inside or not
                        inside = not inside
            
            elif inside:
                totalSize += 1
            
            x += 1
    
    return totalSize

def fillInsideSpace(originalBordersMap: list[list[bool]]) -> list[list[bool]]:
    """ Replace all positions inside of the space by True values """
    bordersMap = copy.deepcopy(originalBordersMap)
    for y in range(len(bordersMap)):
        inside = False
        x = 0
        while (x < len(bordersMap[y])):
            if bordersMap[y][x]:
                ''' NOTE: the logic for this, computing if we're inside or not, 
                    is largely based on part2.py of day10
                '''
                startConnector = computeConnector(originalBordersMap, (x, y))
                
                if startConnector == VERTICAL_CONNECT:
                    # in case we cross a vertical border, we go from inside to outside or the other way around
                    inside = not inside
                else:
                    # we have a corner, so it's more complex
                    sameSideIsOnSide = "left"   # should be a TOP_LEFT_CORNER
                    if startConnector == BOTTOM_LEFT_CORNER:
                        sameSideIsOnSide = "right"
                    
                    # continue up until the first empty space (or end of the line)
                    while (x < len(bordersMap[y])-1 and bordersMap[y][x+1]):
                        x += 1
                    endConnector = computeConnector(originalBordersMap, (x, y))
                    
                    # and then check if we remain on the same side or not
                    if ((endConnector == BOTTOM_RIGHT_CORNER and sameSideIsOnSide != "right") 
                        or 
                        (endConnector == TOP_RIGHT_CORNER and sameSideIsOnSide != "left")):
                        # invert whether we're inside or not
                        inside = not inside
            
            elif inside:
                bordersMap[y][x] = True
            
            x += 1
    
    return bordersMap




with open(INPUT_FILE, 'r') as f:
    # 1) parse the data
    data = [l.strip().split(" ") for l in f.readlines()]
    for i in range(len(data)):
        # cast the number of steps to int
        data[i][1] = int(data[i][1])
        # remove the superfluous parts from the hex color
        data[i][2] = data[i][2][2:-1]
    
    # 2) get all edge points
    edges = generateEdgesFromMoves(data)
    # increase all edges such that all of them become positive
    # --> first get lowest X and lowest Y, then increase all by that amount
    minX, minY = edges[0]
    for i in range(1, len(edges)):
        currX, currY = edges[i]
        if (currX < minX):
            minX = currX
        if (currY < minY):
            minY = currY
    # then add enough so the coordinates start at 0 and only go positive
    incrementX = -minX
    incrementY = -minY
    for i in range(len(edges)):
        currX, currY = edges[i]
        edges[i] = (currX + incrementX, currY + incrementY)
    
    # 3) create the map with the border
    borders = createMapWithBorderOf(edges)
    
    # DEBUG
    if (DEBUG):
        print(f"Size of map: {len(borders)}x{len(borders[0])}")
        print(f"BORDERS MAP:")
        printBorders(borders)
        print("\n----------------------\n")
    
    # 4) compute how many tiles are on the border and inside
    terrainSize = computeSpaceOccupiedBy(borders)
    # 5) give the result of first approach
    print(f"Approach 1: \nExactly {terrainSize} cubic meters of lava fit in the lagoon\n")
        
    # 5) compute the map where the inside is filled in
    filledInMap = fillInsideSpace(borders)
    
    # DEBUG
    if (DEBUG):
        print("BORDERS MAP FILLED INSIDE:")
        printBorders(filledInMap)
        print("\n----------------------\n")
    
    # 6) count up the number of filled in spaces
    numberFilledInSpaces = sum([sum(row) for row in filledInMap])
    
    # 7) return the result for the second approach
    print(f"Approach 2: \nNumber of filled-in fields = {numberFilledInSpaces}")
    # ANSWER: 50465