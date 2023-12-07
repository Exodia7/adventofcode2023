
from functools import cmp_to_key

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

def frequencyCount(iterable):
    """ Counts the frequency of each item in the given iterable
    """
    freqCounts = {}
    for item in iterable:
        # get the old count for this value
        oldCount = 0
        if item in freqCounts.keys():
            oldCount = freqCounts[item]
        # increase by 1
        newCount = oldCount + 1
        # and save it again
        freqCounts[item] = newCount
    return freqCounts

def patternScore(hand):
    """ Returns the value in PATTERN_VALUES
        of the pattern corresponding to the hand in 
        the variable "hand"
    """
    # Compute frequency counts with and without jokers
    valueCounts = frequencyCount(hand)
    valueCountsNoJokers = {key: valueCounts[key] for key in valueCounts.keys() if key != 'J'}
    
    # now compute the highest frequency
    numJokers = valueCounts["J"] if "J" in valueCounts.keys() else 0
    highestFreq = max(valueCounts.values())
    aidedHighestFreq = highestFreq
    if highestFreq != 5:
        # 1) compute the highest frequency counts without jokers
        highestFreqNoJokers = max(valueCountsNoJokers.values())
        # 2) do the sum of the highest frequency count without jokers and the number of jokers
        aidedHighestFreq = highestFreqNoJokers + numJokers
    
    if aidedHighestFreq == 5:
        return PATTERN_VALUES["5 of a kind"]
    elif aidedHighestFreq == 4:
        return PATTERN_VALUES["4 of a kind"]
    elif aidedHighestFreq == 3:
        # check what the second highest frequency is
        secondHighestFreqWithoutJokers = sorted(valueCountsNoJokers.values(), reverse=True)[1]
        if secondHighestFreqWithoutJokers == 2:
            return PATTERN_VALUES["full house"]
        else:
            return PATTERN_VALUES["3 of a kind"]
    elif aidedHighestFreq == 2:
        # check what the second highest frequency is
        secondHighestFreqWithoutJokers = sorted(valueCountsNoJokers.values(), reverse=True)[1]
        if secondHighestFreqWithoutJokers == 2:
            return PATTERN_VALUES["2 pairs"]
        else:
            return PATTERN_VALUES["1 pair"]
    else:
        return PATTERN_VALUES["high card"]

def valueScore(value):
    """ Returns the score of the given value, 
        which are scored as follows:
        - all numbers: the same number as score
        - Jack: 1
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
            return 1        # updated
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

def compareHands(hand1, hand2):
    """ Compares the two hands and gives an integer as result:
        - if hand1 is more valuable than hand2, it returns a positive score
        - if hand1 is less valuable than hand2, it returns a negative score
        - if both hands are the same, it returns zero
    """
    # compare the pattern scores between the two hands, where the 'J's act as jokers
    patternScore1 = patternScore(hand1)
    patternScore2 = patternScore(hand2)
    
    # first comparison factor: the patterns
    if (patternScore1 != patternScore2):
        return (patternScore1 - patternScore2) * 1000
    else:
        # second comparison factor: the values in hand, from left to right
        for i in range(len(hand1)):
            if (valueScore(hand1[i]) != valueScore(hand2[i])):
                return valueScore(hand1[i]) - valueScore(hand2[i])
    
    # in case we reach here, the hands are exactly the same
    return 0

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    data = [l.split(" ") for l in lines]
    for i in range(len(data)):
        data[i][1] = int(data[i][1])
    
    # sort based on their strength
    # ALTERNATIVE 1: give an individual score to each entry
    sortedData1 = sorted(data, key=(lambda entry: handScore(entry[0])))
    # ALTERNATIVE 2: use a compare function
    sortedData2 = sorted(data, key=cmp_to_key(lambda item1, item2: compareHands(item1[0], item2[0])))
    
    # then return the winnings by multiplying the ranks (indices + 1) times the bid
    totalWinnings = 0
    for index in range(len(data)):
        rank = index + 1
        bid = data[index][1]
        totalWinnings += rank * bid
    
    print(f"The total winnings of all hands in my set are: {totalWinnings}")
    # ANSWER: 250382098
