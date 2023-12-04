
import re

INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    # discard everything before the numbers (i.e. before the "Card XX:"
    lines = [l[l.find(":")+1:].strip() for l in lines]
    # extract winning numbers and the others
    lines = [[entry.strip() for entry in l.split("|")] for l in lines]
    # then split each part off into a list of ints
    winningNums = [re.split(r" {1,}", line[0].strip()) for line in lines]
    # NOTE: re.split(r" {1,}", string) splits string whenever encountering one or multiple spaces
    winningNums = [[int(num) for num in card] for card in winningNums]
    
    numsWeHave = [re.split(r" {1,}", line[1].strip()) for line in lines]
    numsWeHave = [[int(num) for num in card] for card in numsWeHave]
    
    # now, compute for each item, how many of the winningNums are in the corresponding item of numsWeHave
    numMatches = [sum([winningNums[i][j] in numsWeHave[i] for j in range(len(winningNums[i]))]) for i in range(len(winningNums))]
    
    # finally, to compute how many of each card we have, we have to multiply the matches by the number of times we will have each card
    # initialise a count of how many of eacch card we have
    numCards = [1 for i in range(len(winningNums))]
    # iterate over all cards, computing the number of instances we'll have of each card
    for i in range(len(winningNums)):
        currentMatches = numMatches[i]
        currentMultiplier = numCards[i]
        # add copies of the next currentMatches cards
        for j in range(currentMatches):
            numCards[i+j+1] += currentMultiplier
    
    # finally, compute the total number of scratchcards we will end up with
    totalNumCards = sum(numCards)
    
    print(f"In total, we will end up with {totalNumCards} scratchcards")
    # ANSWER: 8805731