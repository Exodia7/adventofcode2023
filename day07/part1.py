
INPUT_FILE = "input.txt"
PATTERN_VALUES = {
    "5 of a kind": 7,
    "4 of a kind": 6,
    "full house": 5,
    "3 of a kind": 4,
    "2 pairs": 3,
    "1 pair": 2,
    "high card": 1
}

def patternScore(hand):
    """ Returns the value in PATTERN_VALUES
        of the pattern corresponding to the hand in 
        the variable "hand"
    """
    valueCounts = {}
    for value in hand:
        # get the old count for this value
        oldCount = 0
        if value in valueCounts.keys():
            oldCount = valueCounts[value]
        # increase by 1
        newCount = oldCount + 1
        # and save it again
        valueCounts[value] = newCount
    
    # now check what the highest is
    highestFreq = max(valueCounts.values())
    if highestFreq == 5:
        return PATTERN_VALUES["5 of a kind"]
    elif highestFreq == 4:
        return PATTERN_VALUES["4 of a kind"]
    elif highestFreq == 3:
        # check what the second highest frequency is
        secondHighestFreq = sorted(valueCounts.values(), reverse=True)[1]
        if secondHighestFreq == 2:
            return PATTERN_VALUES["full house"]
        else:
            return PATTERN_VALUES["3 of a kind"]
    elif highestFreq == 2:
        # check what the second highest frequency is
        secondHighestFreq = sorted(valueCounts.values(), reverse=True)[1]
        if secondHighestFreq == 2:
            return PATTERN_VALUES["2 pairs"]
        else:
            return PATTERN_VALUES["1 pair"]
    else:
        return PATTERN_VALUES["high card"]

def valueScore(value):
    """ Returns the score of the given value, 
        which are scored as follows:
        - all numbers: the same number as score
        - Jack: 11
        - Queen: 12
        - King: 13
        - Ace: 14
    """
    if value.isdigit():
        return int(value)
    else: 
        value = value.upper()
        if value == 'T':
            # special 1-character representation for ten
            return 10
        elif value == 'J':
            return 11
        elif value == 'Q':
            return 12
        elif value == 'K':
            return 13
        elif value == 'A':
            return 14
        else:
            raise ValueError("All values should be characters from 2-9 or one of the letters T, J, Q, K, A")

def handScore(hand):
    """ Computes the total score of a certain hand.
        The primary valuation factor is the pattern,
        with the secondary valuation factor being the values in the hand, going from left to right.
    """
    pattern = patternScore(hand)
    total = pattern
    for value in hand:
        # free up the last 2 digits for the next value's score
        total *= 100
        # and add that score
        total += valueScore(value)
    return total
    

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    data = [l.split(" ") for l in lines]
    for i in range(len(data)):
        data[i][1] = int(data[i][1])
    
    # sort based on their strength
    data.sort(key=(lambda entry: handScore(entry[0])))
    
    # then return the winnings by multiplying the ranks (indices + 1) times the bid
    totalWinnings = 0
    for index in range(len(data)):
        rank = index + 1
        bid = data[index][1]
        totalWinnings += rank * bid
    
    print(f"The total winnings of all hands in my set are: {totalWinnings}")
    # ANSWER: 248569531