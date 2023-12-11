
INPUT_FILE = "input.txt"
SPACE_SYMBOL = "."
GALAXY_SYMBOL = "#"

def duplicateEmptyRows(data: [[str]]) -> [[str]]:
    """ Creates a new map based on 'data'.
        Every row with only space will be duplicated.
    """
    # copy the input data
    expandedData = [[data[y][x] for x in range(len(data[y]))] for y in range(len(data))] 
    # iterate over the rows
    y = 0
    while (y < len(expandedData)):
        # check if the row is empty
        emptyRow = True
        x = 0
        while (emptyRow and x < len(expandedData[y])):
            if expandedData[y][x] != SPACE_SYMBOL:
                emptyRow = False
            x += 1
        # one-liner alternative
        #emptyRow = all([expandedData[y][x] == SPACE_SYMBOL for x in range(len(expandedData[y]))])
        
        # and add a new row at the same spot only if the previous one was empty
        if emptyRow:
            expandedData.insert(y, [SPACE_SYMBOL for x in range(len(expandedData[y]))])
            y += 2  # skip the row which we just added
        else:
            y += 1
    
    return expandedData

def duplicateEmptyCols(data: [[str]]) -> [[str]]:
    """ Creates a new map based on 'data'.
        Every column with only space will be duplicated.
    """
    # copy the input data
    expandedData = [[data[y][x] for x in range(len(data[y]))] for y in range(len(data))]
    # iterate over the columns
    x = 0
    while (x < len(expandedData[0])):
        # check if the column is empty
        emptyCol = True
        y = 0
        while (emptyCol and y < len(expandedData)):
            if expandedData[y][x] != SPACE_SYMBOL:
                emptyCol = False
            y += 1
        # one-liner alternative:
        #emptyCol = all([expandedData[y][x] == SPACE_SYMBOL for y in range(len(expandedData))])
        
        # and add a new column at the same spot only if the previous one was empty
        if emptyCol:
            for y in range(len(expandedData)):
                expandedData[y].insert(x, ".")
            x += 2  # skip the column which we just added
        else:
            x += 1
    
    return expandedData

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



with open(INPUT_FILE, 'r') as f:
    # 1) parse the input data
    data = [[char for char in l.strip()] for l in f.readlines()]
    
    # 2) duplicate the empty rows/columns
    expandedData = duplicateEmptyRows(data)
    expandedData = duplicateEmptyCols(expandedData)
    
    # 3) find the indices of all galaxies
    galaxies = []
    for y in range(len(expandedData)):
        for x in range(len(expandedData[y])):
            if expandedData[y][x] == GALAXY_SYMBOL:
                galaxies.append((x, y))
    # 4) create all possible pairs
    pairs = []
    for i1 in range(len(galaxies)):
        for i2 in range(i1+1, len(galaxies)):
            pairs.append((galaxies[i1], galaxies[i2]))
    # 5) compute distances between all possible pairs and do the sum of it
    totalDist = 0
    for gal1, gal2 in pairs:
        totalDist += manhattanDistance(gal1, gal2)
    
    # 6) show the result
    print(f"The sum of all the distances between galaxies is {totalDist}")
    # ANSWER: 10228230