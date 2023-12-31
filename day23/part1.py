
import copy

INPUT_FILE = "input.txt"
PATH = "."
FOREST = "#"
SLOPES = ["^", ">", "v", "<"]
VERBOSE = True

def computePossibleNextPositions(map: list[str], currPos: tuple[int]) -> list[tuple[int]]:
    """ Find all neighboring positions we can move to """
    currX, currY = currPos
    currSymbol = map[currY][currX]
    
    if currSymbol in SLOPES:
        # then we can only move downhill (in the direction of the slope)
        match currSymbol:
            case "^":
                return [(currX, currY-1)]
            case ">":
                return [(currX+1, currY)]
            case "v":
                return [(currX, currY+1)]
            case "<":
                return [(currX-1, currY)]
    else:
        # then we can move in each direction, assuming the tile is not forest
        possiblePositions = [(currX-1, currY), (currX+1, currY), (currX, currY-1), (currX, currY+1)]
        i = 0
        while (i < len(possiblePositions)):
            x, y = possiblePositions[i]
            if (y < 0 or y >= len(map) or x < 0 or x >= len(map)) \
                or (map[y][x] == FOREST):
                # we can not move to that position, either because we would move out of the map
                # or because we would move to a forest tile
                del possiblePositions[i]
            else:
                # keep current position, and move to next
                i += 1
        
        # return the valid possible positions
        return possiblePositions

def findLongestPath(map: list[str], startPos: tuple[int], endPos: tuple[int], pathSoFar: list[tuple[int]]):
    """ Finds the longest path from the starting position to the end position while respecting the conditions """
    maxPathLength = 0
    longestPath = []
    pathsToExploreFurther = [[startPos]]
    while len(pathsToExploreFurther) > 0:
        # 1) take the first path
        currPath = pathsToExploreFurther.pop(0)
        lastPos = currPath[-1]
        
        # VERBOSE: print when we reach a new path length
        if (VERBOSE and len(currPath) >= maxPathLength+250):
            maxPathLength = len(currPath)
            print(f"Reached path length of {maxPathLength}")
        
        # 2) check if it's done, and if so, if it's longer than previous max
        if (lastPos == endPos):
            if (len(currPath) > len(longestPath)):
                longestPath = currPath
        else:
            # 3) go one step further
            # 3.1) compute next possible positions from current position
            nextPositions = computePossibleNextPositions(map, lastPos)
            
            # 3.2) go over all possible positions and add one new path to explore for each valid position
            for i in range(len(nextPositions)):
                # check that we don't go back to a position we already went to
                nextPos = nextPositions[i]
                if nextPos not in currPath:
                    # if so, add the new path to the list to explore
                    nextPath = copy.copy(currPath)
                    nextPath.append(nextPos)
                    pathsToExploreFurther.append(nextPath)
            
    # once we have explored everything, return the longest found path
    return longestPath
        



with open(INPUT_FILE, 'r') as f:
    # 1) parse the data
    data = [l.strip() for l in f.readlines()]
    
    # 2) find starting position
    y = 0
    x = 0
    while (x < len(data[y])):
        if data[y][x] == PATH:
            break
        else:
            x += 1
    startPos = (x, y)
    # 3) find target position
    y = len(data)-1
    x = 0
    while (x < len(data[y])):
        if data[y][x] == PATH:
            break
        else:
            x += 1
    endPos = (x, y)
    
    # 4) find longest path from start to end
    longestPath = findLongestPath(data, startPos, endPos, [])
    
    # leave an empty space
    if VERBOSE: print()
    
    # 5) give the length of that path
    print(f"The longest path has exactly {len(longestPath)-1} steps")
    # ANSWER: 2170 (takes ~10 seconds)