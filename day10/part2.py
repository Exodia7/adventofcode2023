
import copy

def findNextTiles(currentTile, allTiles):
    # extract X and Y
    currX = currentTile[0]
    currY = currentTile[1]
    # initialize the list with the two resulting tiles
    nextTiles = [(0, 0), (0, 0)]
    
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
            # list all tiles around this one that are still within the grid
            allSurroundingTiles = []
            if (currY > 0):
                allSurroundingTiles.append((currX, currY-1))
            if (currY < len(allTiles) - 1):
                allSurroundingTiles.append((currX, currY+1))
            if (currX > 0):
                allSurroundingTiles.append((currX-1, currY))
            if (currX < len(allTiles[currY]) - 1):
                allSurroundingTiles.append((currX+1, currY))
            
            # and for each such tile, check if they point to this one
            for x, y in allSurroundingTiles:
                nextTilesFromSurrounding = findNextTiles((x, y), allTiles)
                if (len(nextTilesFromSurrounding) > 0 and currentTile in nextTilesFromSurrounding):
                        nextTiles.append((x, y))
            # sanity check: make sure there are precisely 2 tiles that point to "S"
            if (len(nextTiles) != 2):
                print(f"WARNING! Found {len(nextTiles)} tiles connected to S, specifically tiles at locations:")
                for tile in nextTiles:
                    print(f" - {tile}")
        case _:
            # none of the above match --> error
            raise ValueError(f"Illegal symbol '{allTiles[currY][currX]}' for tile at index {currentTile}")
   
    # and return the result
    return nextTiles

def findPipeSymbolForStart(startTile, allTiles):
    # extract starting X and Y
    startX = startTile[0]
    startY = startTile[1]
    
    # get the adjacent connected tiles of S
    connectedTiles = findNextTiles(startTile, allTiles)
    # then based on which are inside and which not, return the corresponding symbol:
    up    = (startX,   startY-1)
    down  = (startX,   startY+1)
    left  = (startX-1, startY  )
    right = (startX+1, startY  )
    upConnected = up in connectedTiles
    downConnected = down in connectedTiles
    leftConnected = left in connectedTiles
    rightConnected = right in connectedTiles
    # map it to the right symbol
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
        raise ValueError("Starting tile is not connected to precisely 2 adjacent tiles!")
    
    return resultSymbol

def splitCornersIntoSides(currentTile, allTiles):
    # extract X and Y
    currX = currentTile[0]
    currY = currentTile[1]
    
    # split up the four diagonal corners into the two sides (inside and outside)
    topLeftCorner     = (currX-1, currY-1)
    topRightCorner    = (currX+1, currY-1)
    bottomLeftCorner  = (currX-1, currY+1)
    bottomRightCorner = (currX+1, currY+1)
    insideCorners = []
    outsideCorners = []
    # IMPORTANT: 
    #   we don't know for sure yet which is inside and 
    #   which is outside, but for now we just partition it
    match allTiles[currY][currX]:
        case "|":
            insideCorners = [topLeftCorner, bottomLeftCorner]
            outsideCorners = [topRightCorner, bottomRightCorner]
        case "-":
            insideCorners = [topLeftCorner, topRightCorner]
            outsideCorners = [bottomLeftCorner, bottomRightCorner]
        case "L":
            insideCorners = [topRightCorner]
            outsideCorners = [topLeftCorner, bottomLeftCorner, bottomRightCorner]
        case "J":
            insideCorners = [topLeftCorner]
            outsideCorners = [topRightCorner, bottomLeftCorner, bottomRightCorner]
        case "7":
            insideCorners = [bottomLeftCorner]
            outsideCorners = [topLeftCorner, topRightCorner, bottomRightCorner]
        case "F":
            insideCorners = [bottomRightCorner]
            outsideCorners = [topLeftCorner, topRightCorner, bottomLeftCorner]
        case ".":   # ground tile
            insideCorners = []
            outsideCorners = [topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner]
        case "S":   # starting tile
            # find the adjacent connected tiles
            connectedTiles = findNextTiles(currentTile, allTiles)
            # check which corners are inside and outside for those
            insideCorners1, outsideCorners1 = splitCornersIntoSides(connectedTiles[0], allTiles)
            insideCorners2, outsideCorners2 = splitCornersIntoSides(connectedTiles[1], allTiles)
            ''' ideal case: they have some corners in common
                e.g.       |                  F
                    -S- or S or FSJ or LSJ or S
                           |                  L
                    --> then it's simply the concatenation of the sides which have some corners in common
                    Note: this is always the case if the tiles are on opposite sides of S
                
                otherwise: they don't have any corners in common
                e.g.
                     F
                    FS
                    
                    --> then, take the middle between the corners that are inside/outside,
                    e.g.                      Y                                   Y
                    X                        YF                                  ZF
                   XFS  for the left F and    S  for the top F  which gives:    XFS   where at Z both X and Y are common
                   
                   --> those with middles in common can be put together
                   
                   
                   REPLACE S by the thing it represents!!!!!
            '''
            
            
        case _:
            # none of the above match --> error
            raise ValueError(f"Illegal symbol '{allTiles[currY][currX]}' for tile at index {currentTile}")

def findTilesInsideLoop(startTile, allTiles):
    # extract starting X and Y
    startX = startingTile[0]
    startY = startingTile[1]
    
    # split up the four diagonal corners into the two sides
    topLeftCorner     = (startX-1, startY-1)
    topRightCorner    = (startX+1, startY-1)
    bottomLeftCorner  = (startX-1, startY+1)
    bottomRightCorner = (startX+1, startY+1)
    insideCorners = []
    outsideCorners = []
    # IMPORTANT: 
    #   we don't know for sure yet which is inside and 
    #   which is outside, but for now we just partition it
    match allTiles[startY][startX]:
        case "|":
            insideCorners = [topLeftCorner, bottomLeftCorner]
            outsideCorners = [topRightCorner, bottomRightCorner]
        case "-":
            insideCorners = [topLeftCorner, topRightCorner]
            outsideCorners = [bottomLeftCorner, bottomRightCorner]
        case "L":
            insideCorners = [topRightCorner]
            outsideCorners = [topLeftCorner, bottomLeftCorner, bottomRightCorner]
        case "J":
            insideCorners = [topLeftCorner]
            outsideCorners = [topRightCorner, bottomLeftCorner, bottomRightCorner]
        case "7":
            insideCorners = [bottomLeftCorner]
            outsideCorners = [topLeftCorner, topRightCorner, bottomRightCorner]
        case "F":
            insideCorners = [bottomRightCorner]
            outsideCorners = [topLeftCorner, topRightCorner, bottomLeftCorner]
        case ".":   # ground tile
            insideCorners = []
            outsideCorners = [topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner]
        case "S":   # starting tile
            ''' TODO SOMEHOW '''
        case _:
            # none of the above match --> error
            raise ValueError(f"Illegal symbol '{allTiles[currY][currX]}' for tile at index {currentTile}")
    
    # Then, propagate the areas without crossing any loop items
    insideArea = []
    i = 0
    while (i < len(insideCorners)):
        # from here, propagate
        addedArea, hitBorder = propagateInsideArea(insideCorners[i])
        if hitBorder:
            # this means what we thought was the inside part was actually the outside part
            # --> take the other side and expand it to find the inside part
            insideArea = []
            insideCorners = outsideCorners
            i = 0
        else:
            # add all tiles from the added area to the inside area
            for tile in addedArea:
                if tile not in insideArea:
                    insideArea.append(tile)
        
def getAdjacentTiles(currentTile, allTiles):
    # extract x, y
    currX = currentTile[0]
    currY = currentTile[1]
    # initialize list of adjacent tiles
    adjacentTiles = []
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
    startSymbol = "S"
    xS = -1
    yS = 0
    while (yS < len(allTiles)):
        if (startSymbol in allTiles[yS]):
            xS = allTiles[yS].index(startSymbol)
            break
        else:
            yS += 1
    # 2) create a map denoting all parts of the loop
    loopTiles = {(xS, yS): findNextTiles((xS, yS), allTiles)}
    toExplore = copy.deepcopy(loopTiles[(xS, yS)])
    # 2.1) reuse the breadth-first search of the tiles
    while (len(toExplore) > 0):
        curr = toExplore.pop(0)
        if curr in loopTiles:
            # once we encounter a tile we've already seen, we have completed the loop
            break
        else:
            # and add the next tile (the one in the direction we are going in, not the one we come from) to the list that we still need to explore
            tile1, tile2 = findNextTiles(curr, allTiles)
            tileWeGoTo = tile1
            tileWeComeFrom = tile2
            if (tile1 in loopTiles.keys()):
                tileWeGoTo = tile2
                tileWeComeFrom = tile1
            # add the tile we go to to the ones still to explore
            toExplore.append(tileWeGoTo)
            
            # and add the current tile in the tiles that are part of the loop
            loopTiles[curr] = [tileWeGoTo, tileWeComeFrom]
            # NOTE: this way, we can only follow loopTiles[key][0] for traversing the loop one way, and loopTiles[key][1] goes the other way
    # 2.2) reduce the tiles to only the loop and everything else is ground
    transformedTiles = [["." if (x, y) not in loopTiles.keys() else allTiles[y][x] for x in range(len(allTiles[y]))] for y in range(len(allTiles))]
    # 2.3) replace the "S" by an actual pipe symbol
    transformedTiles[yS][xS] = findPipeSymbolForStart((xS, yS), transformedTiles)
    
    
    DEBUG = False
    
    if (DEBUG): 
        print("Transformed tiles:")
        for y in range(len(transformedTiles)):
            for x in range(len(transformedTiles[y])):
                print(transformedTiles[y][x], end='')
            print()
        print("-------------------------")
    
    # 3) find out which items are outside VS inside by propagating everything throughout
    '''
    toExplore = [((0, 0), False)]
    # each item is (location, isInside)
    #   i.e. location = (x, y)
    #       and isInside is True or False based on whether we are currently inside or outside of the main loop
    explored = []
    '''
    
    tilesInside = []
    # NOTE: we know that the first and last row are outside
    for y in range(1, len(transformedTiles)-1):
        # at the border, we are always on the outside
        isInside = False
        x = 0
        while (x < len(transformedTiles[y])):
            if (DEBUG): 
                print(f"{(y-1)*len(transformedTiles[y])+x}. Currently at x={x}, y={y}, symbol={transformedTiles[y][x]} ", end="")
                if not isInside:
                    print("NOT", end="")
                print(f" inside of the loop")
        
            if transformedTiles[y][x] in ["|"]:
                # we hit a border, we switch whether we're inside or not
                isInside = not isInside
                if (DEBUG):
                    print("Switched: now we are ", end='')
                    if not isInside:
                        print("NOT", end='')
                    print(" inside of the loop")
            elif transformedTiles[y][x] in ["F", "L"]:
                sameSideIsOnSide = "left"
                if transformedTiles[y][x] == "L":
                    sameSideIsOnSide = "right"
                # stores on which side the same side as before is when we are on a "-" line
                
                # skip all "-" until we hit a corner
                x += 1
                while (x < len(transformedTiles[y]) and transformedTiles[y][x] == "-"):
                    x += 1
                
                # then, using the symbol we end the line with, check if we are still on the same side or not
                if ((transformedTiles[y][x] == "J" and sameSideIsOnSide != "right") 
                    or 
                    (transformedTiles[y][x] == "7" and sameSideIsOnSide != "left")):
                    # invert whether we're inside or not
                    isInside = not isInside
            
            elif transformedTiles[y][x] == "." and isInside:
                # we're inside and not hitting a wall of the main loop
                tilesInside.append((x, y))
                if (DEBUG):
                    print("    YAY! Added an item inside of the loop")
            else:
                if (transformedTiles[y][x] != "."):
                    print(f"WARNING! Hit unexpected symbol '{transformedTiles[y][x]}' at index x={x}, y={y}")
            
            x += 1
    
    if (DEBUG): print(f"\nThe tiles inside are: {tilesInside}")
    
    print(f"There are {len(tilesInside)} tiles enclosed by the loop")
    # ANSWER: 453
            
    '''
    while len(toExplore) > 0:
        # check whether the current tile is inside
        curr, isInside = toExplore[0]
        currX, currY = curr
        if isInside and transformedTiles[currY][currX] == ".":
            # if the tile is inside and we don't hit a border of the main loop, the tile is truly inside
            tilesInside.append(curr)
        
        # check whether the current tile is a border, in which case we have to flip isInside
        if transformedTiles[currY][currX] in []:
            
        
        # then add the adjacent tiles to the list to explore
        adjacentTiles = getAdjacentTiles(curr, transformedTiles)
    '''
    
    
    '''
    # 2.2) make a boolean map to check if a tile is part of the loop or not
    isPartOfLoop = [[(x, y) in loopTiles.keys() for x in range(len(allTiles[y]))] for y in range(len(allTiles))]
    
    # 3) propagate the items which are outside by filling up everything from the borders
    # 3.1) initialize a map of all tiles outside of the loop
    outsideTiles = [[isPartOfLoop[y][x] for x in range(len(allTiles[y]))] for y in range(len(allTiles))]
    # 3.2) do a list of all border tiles from which to propagate outside tiles
    borderTilesToPropagate = []
    for y in [0, len(allTiles)-1]:
        for x in range(len(allTiles[y])):   # the top and bottom borders
            if allTiles[y][x] == ".":
                borderTilesToPropagate.append((x, y))
            outsideTiles[y][x] = True
    for y in range(len(allTiles)):      # the left and right borders
        for x in [0, len(allTiles[y])-1]:
            if allTiles[y][x] == ".":
                borderTilesToPropagate.append((x, y))
            outsideTiles[y][x] = True
    # 3.3) for each item to propagate the outside area from, propagate as far as we can
    i = 0
    while (i < len(borderTilesToPropagate)):
        # mark that one tile as outside
        curr = borderTilesToPropagate[i]
        currX = curr[0]
        currY = curr[1]
        outsideTiles[currY][currX] = True
        # explore the adjacent tiles
        adjacent = getAdjacentTiles(curr, allTiles)
        for tile in adjacent:
            tileX = tile[0]
            tileY = tile[1]
            if (not tile in borderTilesToPropagate and allTiles[tileY][tileX] == "."):
                # add tiles to the list to explore that are ground and not yet in the list
                borderTilesToPropagate.append(tile)
            # mark each tile we reach as outside
            outsideTiles[tileY][tileX] = True
        i += 1
    # 3.4) TODO - handle special cases where the loop wraps around a section without it being inside
    
    # 4) return the result
    numInsideTiles = 0
    for y in range(len(allTiles)):
        for x in range(len(allTiles[y])):
            if not outsideTiles[y][x]:
                numInsideTiles += 1
    '''
    
    #print(f"There are {numInsideTiles} tiles enclosed by the loop")
    # ANSWER: 