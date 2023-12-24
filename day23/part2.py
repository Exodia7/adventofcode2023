
import copy
from functools import lru_cache
from pprint import PrettyPrinter
from typing import Union

INPUT_FILE = "input.txt"
PATH = "."
FOREST = "#"
SLOPES = ["^", ">", "v", "<"]
DEBUG = True

@lru_cache
def computePossibleNextPositions(map: tuple[str], currPos: tuple[int]) -> list[tuple[int]]:
    """ Find all neighboring positions we can move to """
    currX, currY = currPos
    currSymbol = map[currY][currX]
    
    if currSymbol in SLOPES:
        print("SLOPE")
        
        # then we can only move downhill (in the direction of the slope)
        possiblePosition = None
        ''' # GOING IN THE OPPOSITE DIRECTION COMPARED TO THE SLOPE DIRECTION
        match currSymbol:
            case "^":
                possiblePosition = [(currX, currY+1)]
            case ">":
                possiblePosition = [(currX-1, currY)]
            case "v":
                possiblePosition = [(currX, currY-1)]
            case "<":
                possiblePosition = [(currX+1, currY)]
        ''' #GOING IN THE DIRECTION OF THE SLOPE
        match currSymbol:
            case "^":
                possiblePosition = [(currX, currY-1)]
            case ">":
                possiblePosition = [(currX+1, currY)]
            case "v":
                possiblePosition = [(currX, currY+1)]
            case "<":
                possiblePosition = [(currX-1, currY)]

        return possiblePosition
        '''
        # only return it if it has not yet been visited
        if possiblePosition not in visited:
            return possiblePosition
        else:
            return []
        '''
    else:
        # then we can move in each direction, assuming the tile is not forest
        possiblePositions = []
        if (currX > 0 and map[currY][currX-1] != FOREST):   # and (currX-1, currY) not in visited):
            possiblePositions.append((currX-1, currY))
        if (currX < len(map[currY])-1 and map[currY][currX+1] != FOREST):   # and (currX+1, currY) not in visited):
            possiblePositions.append((currX+1, currY))
        if (currY > 0 and map[currY-1][currX]!= FOREST):    # and (currX, currY-1) not in visited):
            possiblePositions.append((currX, currY-1))
        if (currY < len(map)-1 and map[currY+1][currX] != FOREST):  # and (currX, currY+1) not in visited):
            possiblePositions.append((currX, currY+1))
        ''' ALTERNATIVE
        possiblePositions = [(currX-1, currY), (currX+1, currY), (currX, currY-1), (currX, currY+1)]
        i = 0
        while (i < len(possiblePositions)):
            x, y = possiblePositions[i]
            if (y < 0 or y >= len(map) or x < 0 or x >= len(map)) \
                or (map[y][x] == FOREST) \
                or ((x, y) in visited):
                # we can not move to that position, either because we would move out of the map,
                # because we would move to a forest tile or because we already visited the tile
                del possiblePositions[i]
            else:
                # keep current position, and move to next
                i += 1
        '''
        
        # return the valid possible positions
        return possiblePositions

'''
def findLongestPath(map: list[str], startPos: tuple[int], endPos: tuple[int]):          #, neighborsCache: dict[tuple[int], list[tuple[int]]], pathSoFar: list[tuple[int]]):
    """ Finds the longest path from the starting position to the end position while respecting the conditions """
    maxPathLength = 0
    longestPath = []
    pathsToExploreFurther = [([startPos], [])]
    lastPos = (-1, -1)
    lastLastPos = (-1, -1)
    while len(pathsToExploreFurther) > 0:
        # 1) take the first path
        currPath, currVisited = pathsToExploreFurther.pop(0)
        lastLastPos = lastPos
        lastPos = currPath[-1]
        
        # VERBOSE: print when we reach a new path length
        if (VERBOSE and len(currPath) >= maxPathLength+1):    #250):
            maxPathLength = len(currPath)
            print(f"Reached path length of {maxPathLength}")
        
        # 2) check if it's done, and if so, if it's longer than previous max
        if (lastPos == endPos):
            if (len(currPath) > len(longestPath)):
                longestPath = currPath
        else:
            # 3) go one step further
            # 3.1) compute next possible positions from current position
            nextPositions = computePossibleNextPositions(tuple(map), lastPos)   #, tuple(currPath))
            #nextPositions = neighborsCache[lastPos]
            # 3.2) append the node to the visited nodes in case it is at a crossroad
            #       --> it can only occur again if it was at a crossroad
            if len(nextPositions) > 2:
                currVisited.append(lastPos)
            
            # 3.3) go over all possible positions and add one new path to explore for each valid position
            for i in range(len(nextPositions)):
                # check that we don't go back to a position we already went to
                nextPos = nextPositions[i]
                if nextPos != lastLastPos and nextPos not in currVisited:
                    # if so, add the new path to the list to explore
                    nextPath = copy.copy(currPath)
                    nextPath.append(nextPos)
                    pathsToExploreFurther.append((nextPath, copy.copy(currVisited)))
            
    # once we have explored everything, return the longest found path
    return longestPath
        
def precomputeNeighborPositions(map: list[str]) -> dict[tuple[int], list[tuple[int]]]:
    """ Pre-compute a dictionary which at every non-forest node,
        stores the non-forest nodes above, below, left and right of it
    """
    neighborsCache = {}
    for y in range(len(map)):
        for x in range(len(map)):
            if map[y][x] != FOREST:
                # compute neighbors and save them
                pos = (x, y)
                neighborsCache[pos] = computePossibleNextPositions(tuple(map), pos)
    
    return neighborsCache
'''

def reduceMapToCrossroads(map: list[str], startPos: tuple[int], endPos: tuple[int]) -> dict[tuple[int], list[tuple[tuple[int] | int]]]:
    """ Reduce the given map to only the crossroad positions.
        Returns a dictionary with as:
        - keys = the crossroad cell
        - value = the list of other crossroad positions that can be reached directly from there,
                along with the distance to reach it
    """
    # 0) initialize some variables
    tupleMap = tuple(map)
    transitions = {}
    
    # 1) setup and start the exploration
    toExplore = [startPos]
    explored = []
    while len(toExplore) > 0:
        # get the current node and its neighbors
        currPos = toExplore.pop(0)
        neighbors = computePossibleNextPositions(tupleMap, currPos)
        # prepare the search
        explored.append(currPos)
        # explore each neighbor until we find the next crossroad
        for i in range(len(neighbors)):
            nextPos = neighbors[i]
            distFromCurrToNextPos = 1
            nextPosNeighbors = computePossibleNextPositions(tupleMap, nextPos)
            
            if (nextPos not in explored):
                # search either the ending position or a crossroad
                while nextPos != endPos and len(nextPosNeighbors) == 2:   # Note: if we ever get exactly 1 neighbor, we hit a dead end, so we can stop
                    # find the neighbor that goes forward
                    forwardNeighbor = None
                    if (nextPosNeighbors[0] in explored and nextPosNeighbors[1] not in explored):
                        forwardNeighbor = nextPosNeighbors[1]
                    elif (nextPosNeighbors[0] not in explored and nextPosNeighbors[1] in explored):
                        forwardNeighbor = nextPosNeighbors[0]
                    else:
                        raise Exception("Something is wrong, either both neighbors are not yet visited or neither")
                    
                    # add the previous node to the nodes we visited
                    explored.append(nextPos)
                    # compute the neighbors with the new node as nextPos
                    nextPos = forwardNeighbor
                    nextPosNeighbors = computePossibleNextPositions(tupleMap, nextPos)
                    distFromCurrToNextPos += 1
                    
                
                if nextPos == endPos or len(nextPosNeighbors) > 2:
                    # we found a new crossroad, add it to the transitions from currPos and to the nodes to explore
                    if (currPos not in transitions.keys()):
                        transitions[currPos] = []
                    transitions[currPos].append((nextPos, distFromCurrToNextPos))
                    if (nextPos not in transitions.keys()):
                        transitions[nextPos] = []
                    transitions[nextPos].append((currPos, distFromCurrToNextPos))
                    
                    toExplore.append(nextPos)
    
    return transitions

def findLongestPathLength(crossroadMap:  dict[tuple[int], list[tuple[tuple[int] | int]]], startPos: tuple[int], endPos: tuple[int]) -> int:
    """ Compute the length of the longest path which does not traverse parts twice """
    maxNumVisited = 0
    
    toExplore = [(startPos, 0, [])]
    # each item has:
    # - index 0: current position
    # - index 1: length of path
    # - index 2: positions already visited in the path
    longestPathLength = -1
    while len(toExplore) > 0:
        # get current situation
        currPos, currPathLength, currVisited = toExplore.pop(0)
        if (DEBUG and len(currVisited) > maxNumVisited):
            maxNumVisited = len(currVisited)
            print(f"\nReached {maxNumVisited} crossroads in path\n")
        # compute possible crossroads to transition to
        possibleNext = crossroadMap[currPos]
        
        # check if that position is the terminal position or not
        if currPos == endPos:
            # check if it's the longest
            if currPathLength > longestPathLength:
                longestPathLength = currPathLength
                if (DEBUG): print(f"New longest path of length {currPathLength} with visited = \n  {currVisited}")
        else:
            for nextPos, nextPosDist in possibleNext:
                if nextPos not in currVisited:
                    # add the subpath currPos -> nextPos to the path
                    nextVisited = copy.copy(currVisited)
                    nextVisited.append(currPos)
                    nextPathLength = currPathLength + nextPosDist
                    # and add the next situation to explore
                    toExplore.append((nextPos, nextPathLength, nextVisited))
    
    return longestPathLength



with open(INPUT_FILE, 'r') as f:
    # 1) parse the data
    data = [l.strip() for l in f.readlines()]
    # 1.1) PART 2 - transform all slopes to paths
    for i in range(len(data)):
        for SLOPE_SYMBOL in SLOPES:
            data[i] = data[i].replace(SLOPE_SYMBOL, PATH)
    
    # 2) find starting position
    y = 0
    x = 0
    while (x < len(data[y])):
        if data[y][x] == PATH:
            break
        else:
            x += 1
    startPos = (x, y)
    # 3) find ending position
    y = len(data)-1
    x = 0
    while (x < len(data[y])):
        if data[y][x] == PATH:
            break
        else:
            x += 1
    endPos = (x, y)
    
    # 2) reduce the whole map to a simple set of transitions, starting at the initial state.
    #   the idea is to reduce it to only the crossroad path cells,
    #   such as to know for each crossroad cell to which other cells it leads
    reducedMap = reduceMapToCrossroads(data, startPos, endPos)
    
    # DEBUG
    if (DEBUG):
        pp = PrettyPrinter()
        print(f"\n\nREDUCED MAP ({len(reducedMap.keys())} keys):")
        pp.pprint(reducedMap)
        print("\n")
    
    # 3) compute which path is the longest based on this representation of the paths
    longestPathLength = findLongestPathLength(reducedMap, startPos, endPos)
    
    # 4) return the result
    print(f"\nThe longest path has {longestPathLength} steps")
    # ANSWER: 6502