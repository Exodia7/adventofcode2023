
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

def findPipeSymbolForStart(startTile, allTiles):
    """ Find and return which symbol the starting symbol should actually be
        to have a working cycle with the loop
    """
    # extract starting X and Y
    startX, startY = startTile
    
    # get the adjacent connected tiles of S
    connectedTiles = findConnectedTiles(startTile, allTiles)
    # check which tiles these are from up/down/left/right
    upConnected    = (startX, startY-1) in connectedTiles
    downConnected  = (startX, startY+1) in connectedTiles
    leftConnected  = (startX-1, startY) in connectedTiles
    rightConnected = (startX+1, startY) in connectedTiles
    # and map it to the right symbol that does these connections
    resultSymbol = ""
    if (upConnected and downConnected):
        resultSymbol = "|"
    elif (leftConnected and rightConnected):
        resultSymbol = "-"
    elif (upConnected and rightConnected):
        resultSymbol = "L"
    elif (upConnected and leftConnected):
        resultSymbol = "J"
    elif (downConnected and leftConnected):
        resultSymbol = "7"
    elif (downConnected and rightConnected):
        resultSymbol = "F"
    else:
        raise ValueError("Starting tile is not connected to 2 adjacent tiles!")
    
    return resultSymbol

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

def printAllTiles(allTiles):
    """ Helper method to print the tiles """
    for y in range(len(allTiles)):
        for x in range(len(allTiles[y])):
            print(allTiles[y][x], end='')
        print()



INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    allTiles = [[char for char in l.strip()] for l in f.readlines()]
    
    # parse all transitions in the main loop
    # 1) find index of S
    startSymbol = "S"
    xS = -1
    yS = 0
    while (yS < len(allTiles)):
        if (startSymbol in allTiles[yS]):
            xS = allTiles[yS].index(startSymbol)
            break
        else:
            yS += 1
    # 2) create a map with only the loop itself
    loopTiles = [(xS, yS)]
    toExplore = findConnectedTiles((xS, yS), allTiles)
    # 2.1) reuse the breadth-first search of the tiles
    while (len(toExplore) > 0):
        curr = toExplore.pop(0)
        if curr in loopTiles:
            # once we encounter a tile we've already seen, we have completed the loop
            break
        else:
            # add the current tile in the tiles that are part of the loop
            loopTiles.append(curr)
            
            # and add the next tile (the one in the direction we are going in, not the one we come from) to the list that we still need to explore
            tile1, tile2 = findConnectedTiles(curr, allTiles)
            if tile1 in loopTiles:
                toExplore.append(tile2)
            else:
                toExplore.append(tile1)
    
    # 2.2) reduce the tiles to only the loop and everything else is ground
    transformedTiles = [["." for x in range(len(allTiles[y]))] for y in range(len(allTiles))]
    for x, y in loopTiles:
        transformedTiles[y][x] = allTiles[y][x]
    # 2.3) replace the "S" by an actual pipe symbol
    transformedTiles[yS][xS] = findPipeSymbolForStart((xS, yS), transformedTiles)
    
    # 3) go through all tiles and extract only the internal tiles
    tilesInside = []
    # NOTE: we know that the first and last row are outside
    for y in range(1, len(transformedTiles)-1):
        # at the border, we are always on the outside
        isInside = False
        x = 0
        while (x < len(transformedTiles[y])):
            if transformedTiles[y][x] in ["|"]:
                # we hit a vertical border, hence switch whether we're inside or not
                isInside = not isInside
            
            elif transformedTiles[y][x] in ["F", "L"]:
                # we hit a corner, so we need to see how the line ends to see if we switched side or not
                sameSideIsOnSide = "left"
                if transformedTiles[y][x] == "L":
                    sameSideIsOnSide = "right"
                # stores on which side the same side as before is when we are on a "-" line
                
                # skip all "-" until we hit a corner again
                x += 1
                while (x < len(transformedTiles[y]) and transformedTiles[y][x] == "-"):
                    x += 1
                
                # then, using the symbol we end the line with, check if we are still on the same side as before or not
                if ((transformedTiles[y][x] == "J" and sameSideIsOnSide != "right") 
                    or 
                    (transformedTiles[y][x] == "7" and sameSideIsOnSide != "left")):
                    # invert whether we're inside or not
                    isInside = not isInside
            
            elif transformedTiles[y][x] == "." and isInside:
                # we're inside and not hitting a wall of the main loop
                tilesInside.append((x, y))
            
            # go to next item
            x += 1
    
    # 4) give the number of tiles we found inside
    print(f"There are {len(tilesInside)} tiles enclosed by the loop")
    # ANSWER: 453