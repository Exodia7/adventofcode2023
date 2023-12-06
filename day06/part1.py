
import re

INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    lines = f.readlines()
    
    # parse the times and record distances for each race
    times = [int(num) for num in re.split(r" {1,}", lines[0][len("Time:"):].strip())]
    recordDistances = [int(num) for num in re.split(r" {1,}", lines[1][len("Distance:"):].strip())]
    
    # initialize the number of ways to win in each race
    numWaysToWin = [0 for i in range(len(times))]
    # and compute the actual number of ways to win
    for raceIndex in range(len(times)):
        totalTime = times[raceIndex]
        recordDist = recordDistances[raceIndex]
        
        for i in range(1, totalTime):
            # no need to try holding the button for 0 and totalTime milliseconds as in both cases, the boat doesn't move at all
            speed = i   # in millimeters/second
            distance = speed * (totalTime - i)
            
            if distance > recordDist:
                numWaysToWin[raceIndex] += 1
    
    # finally, return the multiplication of the number of ways to win for each race
    result = 1
    for n in numWaysToWin:
        result *= n
    
    print(f"The product of the number of ways to beat the record in each race is {result}")
    # ANSWER: 252000