
from enum import Enum

INPUT_FILE = "test.txt"
MAX_NUM_MOVES_IN_SAME_DIR = 3
VERBOSE = True

# same as in day16:
class Direction(Enum):
    RIGHT = 0
    DOWN  = 1
    LEFT  = 2
    UP    = 3

# same as in day16:
def canMoveInDirection(layout: list[str], pos: tuple[int], direction: Direction) -> bool:
    """ Compute and return whether it is possible to move one space 
        in the given direction starting from the given position
    """
    x, y = pos
    match direction:
        case Direction.RIGHT:
            return x < len(layout[0]) - 1
        case Direction.LEFT:
            return x > 0
        case Direction.DOWN:
            return y < len(layout) - 1
        case Direction.UP:
            return y > 0

# same as in day16:
def moveInDirection(pos: tuple[int], direction: Direction) -> tuple[int]:
    """ Compute and return which position is reached by moving one space 
        in the given direction starting from the given position
    """
    x, y = pos
    match direction:
        case Direction.RIGHT:
            return (x+1, y)
        case Direction.LEFT:
            return (x-1, y)
        case Direction.DOWN:
            return (x, y+1)
        case Direction.UP:
            return (x, y-1)

def computePossibleNextDirections(heatLossMap: list[int], pos: tuple[int], direction: Direction, remainingStepsInSameDir: int) -> list[Direction]:
    """ Computes the possible directions we can move in based on the current situation """
    # first, add the directions if we take a turn
    possibleNextDirs = [Direction((direction.value + 1) % 4), Direction((direction.value - 1) % 4)]
    # then, also add the current direction if we can still move in that direction
    if (remainingStepsInSameDir > 0):
        possibleNextDirs.append(direction)
    
    return possibleNextDirs

def findShortestPathLength(heatLossMap: list[int], startPos: tuple[int], targetPos: tuple[int]) -> int:
    """ Finds the shortest path (in terms of heat loss as path weights) 
        between the given starting position and the target position.
        Returns the path length of that path, or -1 if no such path exists
    """
    toExplore = [(startPos, Direction.RIGHT, MAX_NUM_MOVES_IN_SAME_DIR)]
    shortestDistances = {startPos: 0}
    numExplored = 0
    while (len(toExplore) > 0):
        if (VERBOSE and numExplored % 100 == 0): print(f"Exploring node #{numExplored}")
    
        # 1) get current node, direction and number of remaining steps in the same direction
        currPos, currDir, remainingStepsInCurrDir = toExplore.pop(0)
        
        # 2) get the next possible nodes we can move to unless we hit the target position
        if (currPos != targetPos):
            # 2.1) compute the directions in which we could move
            possibleNextDirs = computePossibleNextDirections(heatLossMap, currPos, currDir, remainingStepsInCurrDir)
            # 2.2) for each possible direction, check if the node we would move to exists
            possibleNext = []
            for nextDir in possibleNextDirs:
                # make sure we would still be within the map
                if (canMoveInDirection(heatLossMap, currPos, nextDir)):
                    nextPos = moveInDirection(currPos, nextDir)
                    # compute the distance of the step we just took
                    nextX, nextY = nextPos
                    distToNext = shortestDistances[currPos] + heatLossMap[nextY][nextX]
                    # check if that is shorter than the previous distance to this position
                    if (nextPos not in shortestDistances.keys() or shortestDistances[nextPos] >= distToNext):
                        ''' NOTE: it is crucial to have a ">=" in the if above.
                                Indeed, this is to compute the shortest distances from a node even if the current path
                                has the same length as a previous one, as the direction and number of steps remaining in that direction
                                may be different for that second path with the same length
                        '''
                        shortestDistances[nextPos] = distToNext
                        # and add this node to the ones to explore
                        # the number of remaining steps in this direction is reduced by 1 unless we changed direction
                        remainingStepsInDir = remainingStepsInCurrDir - 1
                        if (nextDir != currDir):
                            remainingStepsInDir = MAX_NUM_MOVES_IN_SAME_DIR - 1
                        
                        toExplore.append((nextPos, nextDir, remainingStepsInDir))
        
        numExplored += 1
    
    if (targetPos in shortestDistances):
        return shortestDistances[targetPos]
    else:
        return -1


''' FOR DEBUGGING: '''
def computePathWeight(heatLossMap : list[int], path: list[tuple[int]]) -> int:
    """ Computes the sum of weights of the given path """
    start = 0
    if (path[0] == (0, 0)):
        start = 1
    totalPathWeight = 0
    for i in range(start, len(path)):
        x, y = path[i]
        totalPathWeight += heatLossMap[y][x]
    
    return totalPathWeight

def printMap(heatLossMap: list[int]):
    """ Prints the given map """
    for y in range(len(heatLossMap)):
        for x in range(len(heatLossMap[y])):
            print(heatLossMap[y][x], end='')
        print()

def printPathWithMap(heatLossMap: list[int], path: list[tuple[int]]):
    """ Prints the given map with indications of the given path,
        as in the example in the assignment instructions.
    """
    startPos = (0, 0)
    for y in range(len(heatLossMap)):
        for x in range(len(heatLossMap[y])):
            if ((x, y) == startPos or (x, y) not in path):
                # print the heat loss for the first space
                # and for all spaces not on the path
                print(heatLossMap[y][x], end='')
            else:
                # check in which direction we moved to get to this node
                currNodeIndex = path.index((x, y))
                prevNode = path[currNodeIndex - 1]
                prevX, prevY = prevNode
                symbol = ""
                if (prevX == x):
                    if (prevY == y-1):
                        symbol = "v"
                    elif (prevY == y+1):
                        symbol = "^"
                    else:
                        raise ValueError(f"Can't find symbol for node x={x}, y={y} with previous node x={prevX}, y={prevY}")
                elif (prevY == y):
                    if (prevX == x-1):
                        symbol = ">"
                    elif (prevX == x+1):
                        symbol = "<"
                    else:
                        raise ValueError(f"Can't find symbol for node x={x}, y={y} with previous node x={prevX}, y={prevY}")
                else:
                    raise ValueError(f"Can't find symbol for node x={x}, y={y} with previous node x={prevX}, y={prevY}")
                
                print(symbol, end='')
        print()



with open(INPUT_FILE, 'r') as f:
    # parse the input
    heatLossMap = [[int(char) for char in l.strip()] for l in f.readlines()]
    
    if (VERBOSE):
        print(f"Map has size {len(heatLossMap)} x {len(heatLossMap[0])} (= {len(heatLossMap) * len(heatLossMap[0])})\n")
    
    
    '''
    # DEBUG
    print("Original input:")
    printMap(heatLossMap)
    print("----------------------------------")
    sampleShortestPath = [(0, 0), (1, 0), (2, 0), 
                            (2, 1), (3, 1), (4, 1), (5, 1),
            (5, 0), (6, 0), (7, 0), (8, 0),
                                    (8, 1),
                                    (8, 2), (9, 2), (10, 2),
                                                    (10, 3),
                                                    (10, 4), (11, 4), 
                                                             (11, 5),
                                                             (11, 6),
                                                             (11, 7), (12, 7),
                                                                      (12, 8),
                                                                      (12, 9),
                                                                      (12, 10),
                                                             (11, 10),
                                                             (11, 11),
                                                             (11, 12), (12, 12)]
    sampleShortestPathWeight = computePathWeight(heatLossMap, sampleShortestPath)
    print("Actual shortest path (for test.txt):")
    printPathWithMap(heatLossMap, sampleShortestPath)
    
    print(f"\nLength of actual shortest path: {sampleShortestPathWeight}")
    print("----------------------------------")
    '''
    # compute the length of the shortest path
    startPos = (0, 0)
    targetPos = (len(heatLossMap[0])-1, len(heatLossMap)-1)
    shortestPathLength = findShortestPathLength(heatLossMap, startPos, targetPos)
    
    ''' DEBUG '''
    #print("----------------------------------")
    
    # print the result
    print(f"The length of the shortest path is: {shortestPathLength}")