
from functools import reduce
from operator import and_

INPUT_FILE = "input.txt"

def findNextNumInSeq(sequence):
    """ Uses the method described in the problem to extrapolate the next number
    """
    if (len(sequence) == 0):
        raise ValueError("The sequence needs to have at least one item!")
    elif (reduce(and_, [x == 0 for x in sequence])):
        # if all numbers in the sequence are zero
        return 0
    else:
        # otherwise, get differences
        diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
        # extrapolate next diff
        nextDiff = findNextNumInSeq(diffs)
        # and add the difference to the last number of the sequence
        return sequence[-1] + nextDiff


with open(INPUT_FILE, 'r') as f:
    # parse the input to separate all numbers and parse to int
    lines = [l.strip().split(" ") for l in f.readlines()]
    numbers = [[int(num) for num in seq] for seq in lines]
    
    # compute the next number in the sequence for all input sequences
    nextNumbers = []
    for numSeq in numbers:
        nextNumbers.append(findNextNumInSeq(numSeq))
    
    # compute the sum and print the result
    result = sum(nextNumbers)
    print(f"The sum of the extrapolated next values in each sequence is: {result}")
    # ANSWER: 