
INPUT_FILE = "input.txt"

OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"

DEBUG = False
VERBOSE = False

NUM_ARRANGEMENTS_CACHE = {}

def transformToKey(springConditions: str, sequenceInfo: [int]) -> tuple[str]:
    """ Transform the given spring conditions and sequence info to a hashable type """
    firstPart = springConditions
    secondPart = "".join([str(n) for n in sequenceInfo])
    
    return firstPart + "-" + secondPart

def countNumPossibleArrangementsRecursive(springConditions : str, sequenceInfo: [int], depth=0) -> int:
    """ Counts the number of possible arrangements of the given information on spring conditions.
        Each arrangement has to be valid with respect to the given sequence information.
        Arrangements are obtained by replacing all unknown spaces by actual spring conditions.
    """
    if (len(sequenceInfo) == 0):
        # check if the given info on spring conditions doesn't have any more damaged springs
        numArrangements = -1
        if (springConditions.count(DAMAGED) == 0):
            # if so, there is one possible arrangement here
            #   (one where all UNKNOWN are filled in with OPERATIONAL)
            if (DEBUG): print(f"{' ' * depth}Valid terminal branch with remaining line '{springConditions}'")
            numArrangements = 1
        else:
            if (DEBUG): print(f"{' ' * depth}Invalid terminal with remaining line '{springConditions}'")
            numArrangements = 0
        
        # memorise the result
        NUM_ARRANGEMENTS_CACHE[transformToKey(springConditions, sequenceInfo)] = numArrangements
        return numArrangements
    elif transformToKey(springConditions, sequenceInfo) in NUM_ARRANGEMENTS_CACHE.keys():
        # return the cached result
        return NUM_ARRANGEMENTS_CACHE[transformToKey(springConditions, sequenceInfo)]
    else:
        # there are still sequences
        # sanity check: make sure that the sum of occurences of UNKNOWN and DAMAGED is more than the sum of the sequences
        if (springConditions.count(DAMAGED) + springConditions.count(UNKNOWN) < sum(sequenceInfo)):
            if (DEBUG): print(f"{' ' * depth}Pruning branch due to not enough potential damaged remaining")
            
            # memorise the result and return it
            numArrangements = 0
            NUM_ARRANGEMENTS_CACHE[transformToKey(springConditions, sequenceInfo)] = numArrangements
            return numArrangements
        else:
            # --> handle the next sequence
            # 1) get its length
            nextSeqLength = sequenceInfo[0]
            # 2) try out every possible spot it can be in
            i = 0
            currPossibleSeqLength = 0
            currActualSeqLength = 0
            currSeqStart = 0
            idxFirstDamaged = -1
            totalNumArrangements = 0
            while (i < len(springConditions)):
                # 2.1) modify the length of the currently ongoing sequence of damaged springs
                if (springConditions[i] == OPERATIONAL):
                    # the sequence is interrupted
                    currPossibleSeqLength = 0
                    currActualSeqLength = 0
                else:
                    # one more item in the sequence, be it an UNKNOWN or DAMAGED space
                    if (springConditions[i] == DAMAGED):
                        currPossibleSeqLength += 1
                        currActualSeqLength += 1
                        # and save the first index at which we saw a DAMAGED tile in idxFirstDamaged
                        if (idxFirstDamaged == -1):
                            idxFirstDamaged = i
                    else:   # implicitly: springConditions[i] == UNKNOWN
                        currPossibleSeqLength += 1
                        currActualSeqLength = 0

                # 2.2) sanity check:
                #       if we actually have a longer sequence (of damaged springs) here than the next sequence has to be, this arrangement is impossible --> stop trying to place the sequence further as it will not work
                if currActualSeqLength > nextSeqLength:
                    if (DEBUG): print(f"{' ' * depth}Too large sequence ({currActualSeqLength} > {nextSeqLength}) - pruning")
                    
                    # memorise the result and return it
                    NUM_ARRANGEMENTS_CACHE[transformToKey(springConditions, sequenceInfo)] = totalNumArrangements
                    return totalNumArrangements
                # 2.3) sanity check:
                #       if the first damaged is nextSeqLength items before the current, we can stop here
                #       --> we can not leave out any DAMAGED spaces
                if (idxFirstDamaged != -1 and idxFirstDamaged <= i - nextSeqLength):
                    if (DEBUG): print(f"{' ' * depth}Would skip damaged space (damaged at {idxFirstDamaged}, i={i}) - pruning")
                    # memorise the result and return it
                    NUM_ARRANGEMENTS_CACHE[transformToKey(springConditions, sequenceInfo)] = totalNumArrangements
                    return totalNumArrangements
                
                # 2.4) check if the sequence can be here 
                #       i.e. the sequence has to be long enough + there has to be an 
                #           OPERATIONAL or UNKNOWN right before and after the sequence
                if (currPossibleSeqLength >= nextSeqLength):
                    seqStart = i - nextSeqLength + 1
                    seqEnd = i
                    if ((seqStart == 0 or springConditions[seqStart - 1] != DAMAGED) and
                        (seqEnd == len(springConditions)-1 or springConditions[seqEnd + 1] != DAMAGED)):
                        # we count the number of arrangements if we place the sequence at seqStart
                        # 1) build up the next sequence
                        
                        if (DEBUG):
                            beforeSeq = ""
                            if (seqStart > 0):
                                beforeSeq = springConditions[:seqStart-1] + OPERATIONAL
                            seq = (DAMAGED * nextSeqLength)
                            afterSeq = ""
                            if (seqEnd < len(springConditions)-1):
                                afterSeq = OPERATIONAL + springConditions[seqEnd+2:]
                            newSpringConditions = beforeSeq + seq + afterSeq
                            print(f"{' ' * depth}Depth {depth} - Placing sequence {nextSeqLength} at index {seqStart}, creating: {newSpringConditions}")
                        
                        # 2.3) count the number of ways the remainder of the spring conditions 
                        #       can be fulfilled in
                        remainingSpringCond = springConditions[seqEnd + 2:]
                        # NOTE: we can skip the sequence + 1 more since the sequence has to be terminated by an operational spring
                        remainingSeqInfo = sequenceInfo[1:]
                        totalNumArrangements += countNumPossibleArrangementsRecursive(remainingSpringCond, remainingSeqInfo, depth+1)
                
                i += 1

            # 3) memorise the result and return the total
            NUM_ARRANGEMENTS_CACHE[transformToKey(springConditions, sequenceInfo)] = totalNumArrangements
            
            return totalNumArrangements


with open(INPUT_FILE, 'r') as f:
    # 1) parse the data
    data = [l.strip().split(" ") for l in f.readlines()]
    for i in range(len(data)):
        # separate the sequences of damaged springs
        data[i][1] = data[i][1].split(",")
        for j in range(len(data[i][1])):
            # and map all of the sequences to ints
            data[i][1][j] = int(data[i][1][j])
    # each entry of data corresponds to one line:
    # - index 0 holds the information on the spring conditions, e.g. "???.###"
    # - index 1 holds the information on the sequences of damaged springs, e.g. [1, 1, 3]
    
    # 2) unfold the data
    NUM_REPETITIONS = 5
    for i in range(len(data)):
        data[i][0] = UNKNOWN.join([data[i][0] for j in range(NUM_REPETITIONS)])
        # NOTE: make sure to make a copy of the original to add 4 times
        originalRequirements = [num for num in data[i][1]]
        for j in range(NUM_REPETITIONS-1):
            data[i][1].extend(originalRequirements)
    
    # 3) count the number of possible arrangements for each line
    totalNumArrangements = 0
    for i in range(len(data)):
        springConditions, sequenceInfo = data[i]
        currNumArrangements = countNumPossibleArrangementsRecursive(springConditions, sequenceInfo)
        if (VERBOSE): print(f"line #{i+1}: found {currNumArrangements} arrangements: {springConditions} - {sequenceInfo}\n")
        totalNumArrangements += currNumArrangements
        
        # SHORTER ALTERNATIVE:
        #totalNumArrangements += countNumPossibleArrangementsRecursive(springConditions, sequenceInfo)
    
    # 4) return the result
    print(f"The total number of arrangements of the spring conditions is {totalNumArrangements}")
    # ANSWER: 160500973317706 (takes a few seconds to run on my machine)