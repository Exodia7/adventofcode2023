
INPUT_FILE = "input.txt"
SPACE_SYMBOL = "."
GALAXY_SYMBOL = "#"
SIZE_EMPTY_LINES = 1000000  # 1 million
# NOTE: if SIZE_EMPTY_LINES is set to 2, part2.py will do exactly the same computation as part1.py, i.e. solve part 1 of the challenge

def manhattanDistance(location1: (int), location2: (int)) -> int:
    """ Computes the Manhattan distance between location1 and location2.
        Manhattan distance is defined by:
        
        the sum for all dimensions i of the points of:
            |location1_i - location2_i|
        where |x| represents the absolute value function
            location1_i the i'th coordinate of location1
            location2_i the i'th coordinate of location2
    """
    if (len(location1) != len(location2)):
        raise ValueError("Both locations need to have the same dimension")
    
    return sum([abs(location1[i] - location2[i]) for i in range(len(location1))])

def printMap(data: [[str]]):
    for y in range(len(data)):
        for x in range(len(data[y])):
            print(data[y][x], end='')
        print()

def countNumEmptyRowsAndColsCrossed(location1: (int), location2: (int), emptyRows: [int], emptyCols: [int]) -> int:
    """ Counts the number of empty rows and columns that need 
        to be crossed to get from location1 to location2.
    """
    # extract coordinates such that y1 holds the smaller one
    y1 = location1[1]
    y2 = location2[1]
    if (y2 < y1):
        y1, y2 = y2, y1
    # count the number of rows y that are strictly between y1 and y2
    count = 0
    for y in range(y1+1, y2):
        if y in emptyRows:
            count += 1
    
    # extract coordinates such that x1 holds the smaller one
    x1 = location1[0]
    x2 = location2[0]
    if (x2 < x1):
        x1, x2 = x2, x1
    # count the number of columns x that are strictly between x1 and x2
    for x in range(x1+1, x2):
        if x in emptyCols:
            count += 1
    
    return count



with open(INPUT_FILE, 'r') as f:
    # 1) parse the input data
    data = [[char for char in l.strip()] for l in f.readlines()]
    
    # 2) find the indices of the empty rows and columns
    # 2.1) the rows
    emptyRows = []
    for y in range(len(data)):
        # check if the row is empty
        rowIsEmpty = True
        x = 0
        while (rowIsEmpty and x < len(data[y])):
            if data[y][x] != SPACE_SYMBOL:
                rowIsEmpty = False
            x += 1
        # one-liner alternative
        #rowIsEmpty = all([data[y][x] == SPACE_SYMBOL for x in range(len(data[y]))])
        
        if rowIsEmpty:
            emptyRows.append(y)
    # 2.2) the columns
    emptyColumns = []
    for x in range(len(data[0])):
        # check if the column is empty
        colIsEmpty = True
        y = 0
        while (colIsEmpty and y < len(data)):
            if data[y][x] != SPACE_SYMBOL:
                colIsEmpty = False
            y += 1
        # one-liner alternative:
        #colIsEmpty = all([data[y][x] == SPACE_SYMBOL for y in range(len(data))])
        
        if colIsEmpty:
            emptyColumns.append(x)
    
    # 3) find the indices of all galaxies
    galaxies = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == GALAXY_SYMBOL:
                galaxies.append((x, y))
    # 4) create all possible pairs
    pairs = []
    for i1 in range(len(galaxies)):
        for i2 in range(i1+1, len(galaxies)):
            pairs.append((galaxies[i1], galaxies[i2]))
    
    # 5) iterate over each pair.
    #       for each pair, compute the number of empty rows and columns 
    #       that need to be crossed to reach the other galaxy
    #       Then, the distance will have those spaces multiplied by 1 million,
    #       and all others counting for just 1
    totalDist = 0
    for gal1, gal2 in pairs:
        numEmptyLinesCrossed = countNumEmptyRowsAndColsCrossed(gal1, gal2, emptyRows, emptyColumns)
        normalDist = manhattanDistance(gal1, gal2)
        # empty spaces are spaces that have no galaxy in their row nor col
        numEmptySpaces = numEmptyLinesCrossed
        # normal spaces are spaces that have a galaxy in their row/col
        numNormalSpaces = normalDist - numEmptySpaces
        
        # the actual distance factors in the size of empty rows and columns
        actualDist = numEmptySpaces * SIZE_EMPTY_LINES + numNormalSpaces
        # add that to the total
        totalDist += actualDist
    
    
    # 6) show the result
    print(f"The sum of all the distances between galaxies (with empty rows and columns counting for {SIZE_EMPTY_LINES}) is {totalDist}")
    # ANSWER: 447073334102