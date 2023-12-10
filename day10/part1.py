
def findConnectedTiles(currentTile, allTiles):
    """ Finds and returns the adjacent tiles to which the tile
        at location currentTile is connected to.
        e.g. 
        in the case of "-", it's the tiles immediately 
        on its left and right
    """
    # extract X and Y
    currX = currentTile[0]
    currY = currentTile[1]
    # initialize the list with the two resulting tiles
    nextTiles = [(0, 0), (0, 0)]
    # and set it to the right values according to the symbol
    match allTiles[currY][currX]:
        case "|":
            nextTiles[0] = (currX  , currY-1)   # up tile
            nextTiles[1] = (currX  , currY+1)   # down tile
        case "-":
            nextTiles[0] = (currX-1, currY  )   # left tile
            nextTiles[1] = (currX+1, currY  )   # right tile
        case "L":
            nextTiles[0] = (currX  , currY-1)   # up tile
            nextTiles[1] = (currX+1, currY  )   # right tile
        case "J":
            nextTiles[0] = (currX  , currY-1)   # up tile
            nextTiles[1] = (currX-1, currY  )   # left tile
        case "7":
            nextTiles[0] = (currX  , currY+1)   # down tile
            nextTiles[1] = (currX-1, currY  )   # left tile
        case "F":
            nextTiles[0] = (currX  , currY+1)   # down tile
            nextTiles[1] = (currX+1, currY  )   # right tile
        case ".":   # ground tile
            nextTiles = []
        case "S":   # starting tile
            nextTiles = []
            # find all tiles around this one that are still within the grid
            allSurroundingTiles = getAdjacentTiles(currentTile, allTiles)
            
            # and for each such tile, check if they point to this one
            for x, y in allSurroundingTiles:
                nextTilesFromSurrounding = findConnectedTiles((x, y), allTiles)
                if (len(nextTilesFromSurrounding) > 0 and currentTile in nextTilesFromSurrounding):
                        nextTiles.append((x, y))
            
            # sanity check: make sure there are precisely 2 tiles that point to "S"
            if (len(nextTiles) != 2):
                raise ValueError(f"WARNING! Found {len(nextTiles)} tiles connected to S, whereas there should be exactly 2")
        case _:
            # none of the above match --> error
            raise ValueError(f"Illegal symbol '{allTiles[currY][currX]}' for tile at index {currentTile}")
   
    # and return the result
    return nextTiles

def getAdjacentTiles(currentTile, allTiles):
    """ Helper method to get the tiles surrounding a certain tile """
    # extract x, y
    currX, currY = currentTile
    
    # initialize list of adjacent tiles
    adjacentTiles = []
    # and add all adjacent tiles there are from up, down, left, right (taking borders into account)
    if (currX > 0):
        adjacentTiles.append((currX-1, currY))
    if (currX < len(allTiles[currY])-1):
        adjacentTiles.append((currX+1, currY))
    if (currY > 0):
        adjacentTiles.append((currX, currY-1))
    if (currY < len(allTiles)-1):
        adjacentTiles.append((currX, currY+1))
    
    return adjacentTiles


INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    allTiles = [[char for char in l.strip()] for l in f.readlines()]
    
    # parse all transitions in the main loop
    # 1) find index of S
    target = "S"
    xS = -1
    yS = 0
    while (yS < len(allTiles)):
        if (target in allTiles[yS]):
            xS = allTiles[yS].index(target)
            break
        else:
            yS += 1
    # 2) find the transitions from S
    toExplore = [(tile, 1) for tile in findConnectedTiles((xS, yS), allTiles)]   # for each element, the first item is the location and the second item the distance from S
    distToS = {(xS, yS): 0}
    # 3) do a breadth-first search of the tiles with their distance to the starting tile
    while (len(toExplore) > 0):
        curr, dist = toExplore.pop(0)
        if curr in distToS.keys():
            # once we encounter a tile we've already seen, we have completed the loop - just make sure we take the shortest distance for this tile
            distToS[curr] = min(dist, distToS[curr])
            break
        else:
            # add it to the record of distances
            distToS[curr] = dist
            
            # and add the next tile (the one in the direction we are going in, not the one we come from) to the list that we still need to explore
            tile1, tile2 = findConnectedTiles(curr, allTiles)
            if (tile1 in distToS.keys()):
                toExplore.append((tile2, dist+1))
            else:
                toExplore.append((tile1, dist+1))
    
    # 4) return the largest distance from all nodes we have explored
    maxDistFromS = max(distToS.values())
    print(f"It takes {maxDistFromS} steps to go from the starting position to the point farthest away from it")
    # ANSWER: 6890