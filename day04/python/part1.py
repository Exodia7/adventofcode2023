
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
    # then, compute the score for that number of matches
    scores = [2 ** (matches - 1) if matches > 0 else 0 for matches in numMatches]
    # finally, the total score is the sum of all individual scores
    totalScore = sum(scores)
    
    print(f"In total, the scratchcards are worth {totalScore} points")
    # ANSWER: 25571