
from enum import Enum
from tqdm import tqdm

INPUT_FILE = "input.txt"

class Spaces:
    EMPTY_SPACE = "."
    MIRROR_DIAGONAL = "\\"
    MIRROR_ANTI_DIAGONAL = "/"
    SPLITTER_VERTICAL = "|"
    SPLITTER_HORIZONTAL = "-"

class Direction(Enum):
    # NOTE: do not change the values here, otherwise it will mess up the getUpdatedDirections method below
    RIGHT = 0
    LEFT  = 1
    DOWN  = 2
    UP    = 3

# a dictionary to map from a direction to the inverse direction
invertDirection = {
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,
    Direction.DOWN: Direction.UP,
    Direction.UP: Direction.DOWN
}

# a dictionary to map from direction to the direction after encountering a MIRROR_DIAGONAL space
diagonalDirTransition = {  
    # right -> down, down -> right, up -> left, left -> up
    # i.e. right and down are interchanged and left and up are interchanged
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN : Direction.RIGHT,
    Direction.UP   : Direction.LEFT,
    Direction.LEFT : Direction.UP
}
# NOTE: the anti-diagonal mapping is exactly the same, except the result directions are exactly inverted (rotated by 180 degrees)

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

def moveInDirection(layout: list[str], pos: tuple[int], direction: Direction) -> tuple[int]:
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

def getUpdatedDirections(tileSymbol : str, initialDir: Direction) -> list[Direction]:
    """ Compute and return the updated direction that we will be moving in
        after encountering a tile with the given symbol while going in the
        given direction.
        Note that in the case of SPLITTER_... spaces, there will be 2 directions,
        hence we return a list
    """
    match tileSymbol:
        case Spaces.EMPTY_SPACE:            # no change
            return [initialDir]
        case Spaces.MIRROR_DIAGONAL:        # = \
            # update direction according to the diagonal mapping
            return [diagonalDirTransition[initialDir]]
        case Spaces.MIRROR_ANTI_DIAGONAL:   # = /
            # update direction according to the anti-diagonal mapping (which is the same as the diagonal, except you invert the direction afterwards)
            return [invertDirection[diagonalDirTransition[initialDir]]]
        case Spaces.SPLITTER_VERTICAL:      # = |
            if (initialDir.value < 2):  # left and right
                # splits the beam in two beams
                return [Direction.UP, Direction.DOWN]
            else:   # up and down
                # does nothing
                return [initialDir]
        case Spaces.SPLITTER_HORIZONTAL:    # = -
            if (initialDir.value < 2):  # left and right
                # does nothing
                return [initialDir]
            else:   # up and down
                # splits the beam in two beams
                return [Direction.LEFT, Direction.RIGHT]

def computeExploredTilesIterative(layout: list[str], startingPos: tuple[int], startingDir: Direction) -> list[list[list[Direction]]]:
    """ Computes all the tiles reached from the given starting position going in the given starting direction.
        All the explored tiles will have the direction in which we encountered it 
        saved at its position in the output matrix
    """
    # 0) Setup
    #   initialize the map of explored tiles by setting all tiles to an empty list
    #       (later, each tile will contain the direction in which we have entered the tile)
    exploredTiles = [[[] for x in range(len(layout[y]))] for y in range(len(layout))]
    #   and initialize the list of situations we still need to explore
    toExplore = [(startingPos, startingDir)]
    while len(toExplore) > 0:
        # 1) extract the info of next item to explore
        currPos, currDir = toExplore.pop(0)
        currX, currY = currPos
    
        # 2) check that we haven't already been in the same position and direction already
        if (currDir in exploredTiles[currY][currX]):
            continue
        else:
            # 3) add the current space with current direction to the explored tiles
            exploredTiles[currY][currX].append(currDir)
            
            # 4) compute the direction(s) we will be going in after hitting the current space
            currTileSymbol = layout[currY][currX]
            nextDirections = getUpdatedDirections(currTileSymbol, currDir)
            
            # 5) perform the moves and keep on exploring
            for nextDir in nextDirections:
                # 5.1) check if we can take a step in that direction
                if (canMoveInDirection(layout, currPos, nextDir)):
                    # 5.2) take one step in that direction
                    nextPos = moveInDirection(layout, currPos, nextDir)
                    # 5.3) add those positions to the list to explore
                    toExplore.append((nextPos, nextDir))
    
    return exploredTiles

def computeEnergizedTiles(layout: list[str], startingPos: tuple[int], startingDir: Direction) -> list[list[bool]]:
    """ Computes all the energized tiles based on a single starting beam,
        starting at the top left corner tile, moving towards the right.
    """
    # start the exploration of the energized tiles at the given position, moving in the given direction
    exploredTiles = computeExploredTilesIterative(layout, startingPos, startingDir)
    
    # compute which tiles are energized and which not based on whether we explored the tile or not
    return [[len(exploredTiles[y][x]) > 0 for x in range(len(exploredTiles[y]))] for y in range(len(exploredTiles))]



with open(INPUT_FILE, 'r') as f:
    # parse input
    data = [l.strip() for l in f.readlines()]
    
    # generate all possible starting positions and starting directions
    possibleStartConfigs = []
    for y in range(len(data)):
        # add the configuration on the leftmost column
        startPos = (0, y)
        startDir = Direction.RIGHT
        possibleStartConfigs.append((startPos, startDir))
        
        # and add the configuration on the rightmost column
        startPos = (len(data[y])-1, y)
        startDir = Direction.LEFT
        possibleStartConfigs.append((startPos, startDir))
    for x in range(len(data[0])):
        # add the configuration on the top row
        startPos = (x, 0)
        startDir = Direction.DOWN
        possibleStartConfigs.append((startPos, startDir))
        
        # and add the configuration on the bottom row
        startPos = (x, len(data)-1)
        startDir = Direction.UP
        possibleStartConfigs.append((startPos, startDir))
    
    # iterate over all starting positions, computing the number of energized tiles
    maxNumEnergizedTiles = 0
    progressBar = tqdm(total=len(possibleStartConfigs))
    for startConfig in possibleStartConfigs:
        # extract the info
        startPosition, startDirection = startConfig
        
        # compute which tiles are energized
        energizedTiles = computeEnergizedTiles(data, startPosition, startDirection)
        # compute the number of energized tiles
        numEnergizedTiles = sum([sum(energizedTiles[y]) for y in range(len(energizedTiles))])
        # and save it as max if it's larger than the previous max
        if (numEnergizedTiles > maxNumEnergizedTiles):
            maxNumEnergizedTiles = numEnergizedTiles
        
        # update the progress bar
        progressBar.update(1)
        
    # print the result
    print(f"\n\nThere are {maxNumEnergizedTiles} energized tiles in the initial beam configuration energizing the most tiles")
    # ANSWER: 7943