
from functools import cmp_to_key
from pprint import PrettyPrinter

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
"""
def compareHands(hand1, hand2):
    # get the frequency count for both hands
    freqCounts1 = frequencyCount(hand1)
    freqCounts2 = frequencyCount(hand2)
    '''
    print("DEBUG - ")
    print(f"Frequency counts hand1 = {freqCounts1}")
    print(f"Frequency counts hand2 = {freqCounts2}")
    '''
    # get the count of 'J's in each hand
    numJokers1 = freqCounts1["J"] if "J" in freqCounts1.keys() else 0
    numJokers2 = freqCounts2["J"] if "J" in freqCounts2.keys() else 0
    # then compare the highest frequency counts
    highestFreq1 = max(freqCounts1.values())
    highestFreq2 = max(freqCounts2.values())
    # "aided" highest frequency (taking jokers into account)
    aidedHighestFreq1 = highestFreq1
    if highestFreq1 != 5:
        # 1) compute the highest frequency counts without jokers
        highestFreq1NoJokers = max([freqCounts1[key] for key in freqCounts1.keys() if key != "J"])
        # 2) do the sum of the highest frequency count without jokers and the number of jokers
        aidedHighestFreq1 = highestFreq1NoJokers + numJokers1
    aidedHighestFreq2 = highestFreq2
    if highestFreq2 != 5:
        # 1) compute the highest frequency counts without jokers
        highestFreq2NoJokers = max([freqCounts2[key] for key in freqCounts2.keys() if key != "J"])
        # 2) do the sum of the highest frequency count without jokers and the number of jokers
        aidedHighestFreq2 = highestFreq2NoJokers + numJokers2
    '''
    print("DEBUG - ")
    print("- stats for hand1: ")
    print(f"    highestFreq={highestFreq1}")
    print(f"    numJokers={numJokers1}")
    print(f"    aidedHighestFreq={aidedHighestFreq1}")
    print("- stats for hand2: ")
    print(f"    highestFreq={highestFreq2}")
    print(f"    numJokers={numJokers2}")
    print(f"    aidedHighestFreq={aidedHighestFreq2}")
    '''
    # first comparison factor: total frequency with jokers
    if (aidedHighestFreq1 != aidedHighestFreq2):
        return (aidedHighestFreq1 - aidedHighestFreq2) * 1000
    else:
        # second comparison factor: the values in hand, from left to right
        for i in range(len(hand1)):
            if (valueScore(hand1[i]) != valueScore(hand2[i])):
                return valueScore(hand1[i]) - valueScore(hand2[i])
    
    # in case we reach here, the hands are exactly the same
    return 0
"""
'''
hand1 = 'KKJKK'
hand2 = 'JJJ8J'

print(f"Comparing hands '{hand1}' and '{hand2}' returns: {compareHands(hand1, hand2)}")
'''

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    data = [l.split(" ") for l in lines]
    for i in range(len(data)):
        data[i][1] = int(data[i][1])
    
    # sort based on their strength
    data.sort(key=(lambda entry: handScore(entry[0])))
    # USING a compare function:
    #data.sort(key=cmp_to_key(lambda item1, item2: compareHands(item1[0], item2[0])))

    #pp = PrettyPrinter()
    #pp.pprint([x[0] for x in data])
    
    # then return the winnings by multiplying the ranks (indices + 1) times the bid
    totalWinnings = 0
    for index in range(len(data)):
        rank = index + 1
        bid = data[index][1]
        totalWinnings += rank * bid
    
    print(f"The total winnings of all hands in my set are: {totalWinnings}")
    # ANSWER: 250382098