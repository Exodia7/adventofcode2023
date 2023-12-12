
from tqdm import tqdm   # for progress bar

INPUT_FILE = "input.txt"
OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"

def countContiguousDamaged(info: str) -> [int]:
    """ Returns a count of the number of subsequent damaged springs in info
        e.g.
        "#...###.#.##"    -->    [1, 3, 1, 2]
    """
    contiguousGroups = []
    i = 0
    while (i < len(info)):
        if (info[i] == OPERATIONAL):
            # skip operational springs
            i += 1
        elif (info[i] == DAMAGED):
            # count how many contiguous damaged tiles we have
            groupSize = 0
            while (i < len(info) and info[i] == DAMAGED):
                groupSize += 1
                i += 1
            # add the size to the contiguous groups
            contiguousGroups.append(groupSize)
        else:
            raise ValueError(f"The condition record has to contain only operational spaces (='{OPERATIONAL}') and damaged spaces ('{DAMAGED}')")
    
    return contiguousGroups


def countArrangementsBruteForce(info: str, requirement: [int]) -> int:
    """ Count the number of possible arrangements of the given line 'info'.
        Arrangements are obtained by filling in the unknown spaces with actual values, 
        in a way respecting the requirements of contiguous groups given in 'requirement'
    """
    if (info.count(UNKNOWN) == 0):
        # there's no unknown in the list
        # in this case, we either have 0 or 1 possible arrangements depending on 
        # whether the contiguous groups in the arrangement are the same as the requirement or not
        contiguousGroups = countContiguousDamaged(info)
        
        return (contiguousGroups == requirement)
    else:
        # find the next unknown space
        unknownSpaceIndex = info.index(UNKNOWN)
        # try both possible values for this space and sum the arrangements
        numArrangements = 0
        for replacementSymbol in [DAMAGED, OPERATIONAL]:
            # replace the index with the given symbol
            replacedInfo = info[:unknownSpaceIndex] + replacementSymbol + info[unknownSpaceIndex+1:]
            # and count the number of possible arrangements
            numArrangements += countArrangementsBruteForce(replacedInfo, requirement)
        
        return numArrangements



with open(INPUT_FILE, 'r') as f:
    # parse the data
    data = [l.strip().split(" ") for l in f.readlines()]
    for i in range(len(data)):
        # separate the sequences of damaged springs
        data[i][1] = data[i][1].split(",")
        for j in range(len(data[i][1])):
            # and map all of the sequences to ints
            data[i][1][j] = int(data[i][1][j])
    
    # count the number of possible arrangements of the "?" that respect the sequences of contiguous damaged springs
    totalArrangements = 0
    progressBar = tqdm(total=len(data))
    for i in range(len(data)):
        # update progress bar
        progressBar.update(1)
        
        # do the computations
        row, requirement = data[i]
        numArrangements = countArrangementsBruteForce(row, requirement)
        totalArrangements += numArrangements
    
    # and show result
    print(f"The total number of arrangements that fit the given criteria is: {totalArrangements}")
    # ANSWER: 8419 (takes a bit over a minute to compute)