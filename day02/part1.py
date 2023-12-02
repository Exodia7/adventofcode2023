
INPUT_FILE = "input.txt"

# the maximum number of red, green and blue cubes
MAX_NUM_CUBES = {"red": 12, "green": 13, "blue": 14}

with open(INPUT_FILE, 'r') as f:
    lines = f.readlines()
    
    possibleGames = []
    
    for line in lines:
        # extract the different revelations
        gameId, revelations = line.split(":")
        # split each revelation line into the single sets of revelations
        revelations = revelations.split(";")
        # maintain a boolean of whether the specific game is still possible or not
        lineStillPossible = True
        for revel in revelations:
            if lineStillPossible:
                # split each revelation into the different colors
                colorsRevel = [x.strip() for x in revel.split(",")]
                
                for data in colorsRevel:
                    # for each specific revelation, e.g. "3 red", check that it doesn't violate the rules
                    num, color = data.split(" ")
                    num = int(num)
                    color = color.strip()
                    
                    if num > MAX_NUM_CUBES[color]:
                        lineStillPossible = False
        
        # if we have not found any revelation which is impossible, the game is possible!
        if lineStillPossible:
            # extract game id
            idNum = int(gameId.split(" ")[1].strip())
            # and add it to the list of possibleGames
            possibleGames.append(idNum)
    
    
    print(f"The sum of all possible game ids is: {sum(possibleGames)}")
    # ANSWER: 2348