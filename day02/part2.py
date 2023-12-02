
INPUT_FILE = "input.txt"

# the indices at which to store the count for each color
CUBE_INDEX = {"red": 0, "green": 1, "blue": 2}

with open(INPUT_FILE, 'r') as f:
    lines = f.readlines()
    
    minimumNumCubes = []
    
    for line in lines:
        # extract the different revelations
        gameId, revelations = line.split(":")
        # split each revelation line into the single sets of revelations
        revelations = revelations.split(";")
        
        # append a list of size 3 for the minimum number of each cube
        minimumNumCubes.append([0, 0, 0])
        
        for revel in revelations:
            # split each revelation into the different colors
            colorsRevel = [x.strip() for x in revel.split(",")]
            
            for data in colorsRevel:
                # for each specific revelation, e.g. "3 red", check that it doesn't violate the rules
                num, color = data.split(" ")
                num = int(num)
                color = color.strip()
                
                # replace the maximum if num is higher
                minimumNumCubes[-1][CUBE_INDEX[color]] = max(minimumNumCubes[-1][CUBE_INDEX[color]], num)
    
    
    # Then compute the power of each game
    gamePower = [numCubes[0] * numCubes[1] * numCubes[2] for numCubes in minimumNumCubes]
    sumGamePower = sum(gamePower)
    
    print(f"The sum of the power of all games is: {sumGamePower}")
    # ANSWER: 76008