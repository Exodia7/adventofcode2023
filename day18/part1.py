
from typing import Union

INPUT_FILE = "input.txt"
DEBUG = False


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

def generateEdgesFromData(data: list[list[Union[str, int]]]) -> dict[int, list[int]]:
    """ Based on the given moves to perform, returns a list of the edges with their indices """
    currPos = (0, 0)
    edges = {0: [0, 0]}
    # keys = row indices
    # values = list of column indices at which a border appears
    for i in range(len(data)):
        # extract the next move to perform
        direction = data[i][0]
        numSteps = data[i][1]
        # perform it to get the destination position
        nextPos = performMove(currPos, direction, numSteps)
        
        # DEBUG
        if (DEBUG): print(f"Moving from {currPos} to {nextPos}")
        
        # and add all the borders to the list
        currX, currY = currPos
        nextX, nextY = nextPos
        rangeX = [currX]
        rangeY = [currY]
        if (direction in ["U", "D"]):
            # if we go up or down, we add all values in-between to the list
            rangeY = range(min(currY, nextY), max(currY, nextY)+1)
        else:
            # if we go left or right, we can just add the left-most and right-most number
            rangeX = [min(currX, nextX), max(currX, nextX)]
        
        for x in rangeX:
            for y in rangeY:
                # only add x if it's not yet inside (e.g. if we pass by the same position twice)
                if (y not in edges.keys() or x not in edges[y]):
                    if (DEBUG): print(f"Adding ({x}, {y}) to the list")
                
                    # get the list of the minimum and maximum x value which we have 
                    xMinMax = [x, x]
                    if y in edges.keys():
                        xMinMax = edges[y]
                    
                    if (DEBUG): print(f"Previous xs = {xMinMax}")
                    
                    # insert the new x if it's the new min or new max
                    if (x < xMinMax[0]):
                        xMinMax[0] = x
                    elif (x > xMinMax[1]):
                        xMinMax[1] = x
                    
                    if (DEBUG): print(f"Previous xs (after inserting x) = {xMinMax}")
                    
                    # and add the result back in
                    edges[y] = xMinMax
                else:
                    if (DEBUG): print(f"Not adding it to the list ({x}, {y})")
    
        # finally, update the current position
        currPos = nextPos
    
    return edges

def computeSpaceOccupiedBy(edges: dict[int, list[int]]) -> int:
    """ Computes the size of the shape described by the edges given as parameter, including the edge lines """
    totalSize = 0
    
    for y in edges.keys():
        xs = edges[y]
        
        # sanity check: make sure there are a multiple of 2 borders (always 1 to enter the area, and 1 to exit the area
        if len(xs) % 2 != 0:
            raise ValueError("There should always be a multiple of two as borders on one line!")
        else:
            for i in range(0, len(xs), 2):
                # get the first two borders
                x1 = xs[i]
                x2 = xs[i+1]
                # compute the space occupied between x1 and x2 (including both borders)
                rowSize = x2 - x1 + 1
                # add it to the total
                totalSize += rowSize
    
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
    edges = generateEdgesFromData(data)
    
    # DEBUG
    if (DEBUG): 
        print(edges)
        print("\n----------------------\n")
    
    # 3) compute how many tiles are on the border and inside
    terrainSize = computeSpaceOccupiedBy(edges)
    
    # 4) return the result
    print(f"Exactly {terrainSize} cubic meters of lava fit in the lagoon")
    # TRIES: 56354 (too high, because it doesn't properly take into account shapes such as the hole in the bottom center of:
    '''
        #########
        #       #
        #  ###  #
        #  # #  #
        #### ####
    '''