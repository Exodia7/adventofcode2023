
import math

INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    lines = f.readlines()
    
    # parse the time and record distance for the race
    totalTime = int(lines[0][len("Time:"):].strip().replace(" ", ""))
    recordDist = int(lines[1][len("Distance:"):].strip().replace(" ", ""))
    
    # initialize the number of ways to win
    numWaysToWin = 0
    # and compute the actual number of ways to win
    # NOTE: we know that the distance will be small if we only hold the button very shortly and also if we hold it very long
    # --> find the number of milliseconds where the distance starts being enough and the number of milliseconds where the distance stops being enough, then the number of ways is the difference between the two
    # 1) find the starting number
    ''' HEURISTIC NOTE: 
        Let's say holding the button doesn't take away time from the race time.
        The speed we would need to start at to beat the record distance would be:
            speed * (race time) > (record distance)
        <=> speed > (record distance) / (race time)
        
        Hence, we can use (record distance) / (race time) as lower bound of the time we need to hold the button.
        Indeed, in actuality, all time spent holding down the button reduces the race time. In the equation above, one can see that the speed would need to be greater then (as if "race time" decreases, "speed" needs to increase to balance it out)
        
        This is used in the equation below
    '''
    startNum = math.floor(recordDist / totalTime)
    foundStart = False
    while (not foundStart and startNum < totalTime):
        # no need to try holding the button for 0 and totalTime milliseconds as in both cases, the boat doesn't move at all
        speed = startNum   # in millimeters/second
        distance = speed * (totalTime - startNum)
        
        if distance > recordDist:
            foundStart = True
        else:
            startNum += 1
    # 2) find the ending number
    ''' HEURISTIC NOTE: 
        Let's say that the race itself is not limited by the race time given in the input. The maximum speed we could reach is then the "race time" given as input, if we held on to the button for the whole race.
        We would then need an "actual race time" such that:
            (actual race time) * (max speed) > (record distance)
        and we know that the max speed is "race time", as we can not hold the button longer than that. We then have:
            (actual race time) * (race time) > (record distance)
            (actual race time) > (record distance)/(race time)
        Note that this is the same value as the heuristic above.
        
        In this case, the time that we hold on the button for would be:
            (race time) - (actual race time)
        
        This is used in the equation below
    '''
    endNum = math.ceil(totalTime - (recordDist / totalTime))
    foundEnd = False
    while (not foundEnd and endNum >= startNum):
        # no need to search lower than startNum since we know everything lower is not enough
        speed = endNum   # in millimeters/second
        distance = speed * (totalTime - endNum)
        
        if distance > recordDist:
            foundEnd = True
        else:
            endNum -= 1
    
    # 3) compute the number of ways based on 1) and 2)
    numWaysToWin = endNum - startNum + 1
    # NOTE: the +1 is to include both startNum and endNum
    
    # finally, return the result
    print(f"The number of ways to beat the record of the race is {numWaysToWin}")
    # ANSWER: 36992486